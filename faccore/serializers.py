"""
Copyright (C) 2020-2022 LIG Université Grenoble Alpes


This file is part of FacManager.

FacManager is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

FacManager is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with FacManager. If not, see <https://www.gnu.org/licenses/>

@author Germain Lemasson
"""

from collections import OrderedDict
from rest_framework import serializers, exceptions
from django.contrib.auth import get_user_model

from .models import MachineModel, TrainingLevel, Supply, ReservationType, Availability, Machine, Manager, SupplyUsage, Reservation, Event


class ChoicesField(serializers.Field):
    """Custom ChoiceField serializer field."""

    def __init__(self, choices, **kwargs):
        """init."""
        self._choices = OrderedDict(choices)
        super(ChoicesField, self).__init__(**kwargs)

    def to_representation(self, obj):
        """Used while retrieving value for the field."""
        return self._choices[obj]

    def to_internal_value(self, data):
        """Used while storing value for the field."""
        for i in self._choices:
            if self._choices[i] == data:
                return i
        raise serializers.ValidationError(
            "Acceptable values are {0}.".format(list(self._choices.values())))


class SupplySerializer(serializers.ModelSerializer):
    class Meta:
        model = Supply
        fields = '__all__'


class SupplyUsageSerializer(serializers.ModelSerializer):
    quantity = serializers.DecimalField(max_digits=16, decimal_places=2)

    class Meta:
        model = SupplyUsage
        fields = '__all__'


class SupplyUsagePublicSerializer(SupplyUsageSerializer):
    class Meta:
        model = SupplyUsage
        exclude = ['user']
        read_only_fields = ['__all__']


class MachineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Machine
        fields = '__all__'


class MachineInstanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Machine
        fields = ['id', 'name']


class MachineModelSerializer(serializers.ModelSerializer):
    instances = MachineInstanceSerializer(many=True, read_only=True)

    class Meta:
        model = MachineModel
        fields = ['id', 'name', 'description', 'display_order', 'instances']


class ManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manager
        fields = '__all__'


class AvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Availability
        fields = '__all__'


class ReservationTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReservationType
        fields = '__all__'


class TrainingLevelListSerializer(serializers.ListSerializer):
    """
    Class allowing bulk update of training level
    """

    def update(self, instance, validated_data):
        # Maps for id->instance and id->data item.
        tl_mapping = {tl.id: tl for tl in instance}
        data_mapping = {item['id']: item for item in validated_data}
        ret = []
        for tl_id, data in data_mapping.items():
            tl = tl_mapping.get(tl_id, None)
            if tl is not None:
                ret.append(self.child.update(tl, data))
        return ret


class TrainingLevelSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = TrainingLevel
        read_only_fields = ['machine_model']
        exclude = ['user']
        list_serializer_class = TrainingLevelListSerializer


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'


class ReservationSerializer(serializers.ModelSerializer):
    status = ChoicesField(choices=Reservation.STATUS,
                          default=Reservation.REQUESTED)

    own = serializers.SerializerMethodField()

    class Meta:
        model = Reservation
        fields = '__all__'

    def get_own(self, obj):
        request = self.context.get("request")
        if request.user.is_authenticated:
            return obj.user == request.user
        else:
            return False

    def validate(self, data):
        """
        Method validating the reservation
        """
        user = None
        start_date = data['start_date']
        request = self.context.get("request")
        end_date = data['end_date']
        uses = data['uses']
        rtype = data['reservation_type']
        # Verify that a manager used if not needed
        if(not rtype.need_manager and not data['manager'] is None):
            raise serializers.ValidationError(
                'Manager is not needed', code='invalid')
        # Verify that a manager is used if needed
        if(rtype.need_manager and data['manager'] is None):
            raise serializers.ValidationError(
                'One manager is needed', code='invalid')
        # Verify that each need of the reservation type is fulfilled
        machines_used = uses.copy()
        for machine_model in rtype.needs.all():
            machines_of_model = [
                machine for machine in machine_model.instances.all()]
            matches = [
                machine for machine in machines_of_model if machine in machines_used]
            if len(matches) > 1:
                raise serializers.ValidationError(
                    'Only one instance of ' + str(machine_model) + ' is needed', code='invalid')
            elif len(matches) == 0:
                raise serializers.ValidationError(
                    'One instance of ' + str(machine_model) + ' is needed', code='invalid')
            else:
                machines_used.remove(matches[0])
        # Verify that a machine is not used if not needed
        if len(machines_used) > 0:
            raise serializers.ValidationError(
                'Machines ' + str(machines_used) + ' are not needed', code='invalid')
        # Verify resources avaibilities
        if request and hasattr(request, "user"):
            if not request.user.is_staff and (data['status'] != Reservation.DENIED):
                availinter = Availability.objects.filter(start_date__lte=start_date).filter(
                    end_date__gte=start_date).values('resources')
                resources = [res['resources'] for res in availinter]

                resources_resa = [ma.id for ma in data['uses']]
                if(not data['manager'] is None and not data['manager'].id in resources):
                    raise serializers.ValidationError(
                        'Manager ' + str(data['manager']) + " is not available", code='invalid')
                missing = [r for r in resources_resa if not r in resources]
                if(len(missing) > 0):
                    machine_names = [
                        m.name for m in Machine.objects.filter(pk__in=missing)]
                    raise serializers.ValidationError(str(','.join(machine_names)) + (
                        " is" if len(machine_names) == 1 else " are") + " not available", code='invalid')

        # Verify that this reservation (if not denied) is not in conflit of an other accepted reservation
        if(data['status'] != Reservation.DENIED):
            # start during
            resainter = Reservation.objects.filter(status=Reservation.ACCEPTED).filter(
                start_date__lte=start_date).filter(end_date__gt=start_date)
            # end during
            resainter2 = Reservation.objects.filter(status=Reservation.ACCEPTED).filter(
                start_date__gte=start_date).filter(start_date__lt=end_date)
            if not self.instance is None:
                resainter = resainter.exclude(pk=self.instance.id)
                resainter2 = resainter2.exclude(pk=self.instance.id)
            resainter = resainter | resainter2
            if(resainter.count() != 0):
                for resa in resainter.all():
                    if resa.manager != None and resa.manager == data['manager']:
                        raise serializers.ValidationError(
                            str(resa.manager) + " is not available", code='conflict')
                    for machine in resa.uses.all():
                        if machine in uses:
                            raise serializers.ValidationError(
                                'Conflict using resource ' + str(machine), code='conflict')
        return data


class ReservationPublicSerializer(ReservationSerializer):
    own = serializers.SerializerMethodField()

    class Meta:
        model = Reservation
        exclude = ['user', 'commentary']

    def get_own(self, obj):
        request = self.context.get("request")
        if request.user.is_authenticated:
            return obj.user == request.user
        else:
            return False


class ReservationUsageSerializer(serializers.ModelSerializer):
    status = ChoicesField(choices=Reservation.STATUS,
                          default=Reservation.REQUESTED)
    duration = serializers.SerializerMethodField()

    class Meta:
        model = Reservation
        exclude = ['commentary', 'created_date', 'uses', 'manager']

    def get_duration(self, obj):
        td = obj.end_date - obj.start_date
        return td.seconds / 3600
