from datetime import timedelta, datetime
import dateutil.parser
from collections import OrderedDict
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.core.mail import EmailMultiAlternatives
from django.http import QueryDict
from django.core.exceptions import PermissionDenied
from django.utils import timezone
from django.template.loader import render_to_string
from django.db.models import Prefetch
from django.contrib.auth import get_user_model

from rest_framework import viewsets, mixins, status, serializers, filters, pagination
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.response import Response
from rest_framework.exceptions import ParseError

import email.utils
import json


from .serializers import SupplySerializer, SupplyUsageSerializer, MachineModelSerializer, ManagerSerializer, MachineSerializer, AvailabilitySerializer, ReservationTypeSerializer, TrainingLevelSerializer, TrainingLevelListSerializer, ReservationSerializer, ReservationPublicSerializer, ReservationUsageSerializer, EventSerializer
from .models import MachineModel, TrainingLevel, Supply, ReservationType, Availability, Machine, Manager, SupplyUsage, Reservation, Event

from facusers.permissions import IsAdminOrReadOnly, IsAdminOrIsSelf
from facusers.models import Project


class IsOwnerFilterBackend(filters.BaseFilterBackend):
    """
    Filter that only allows users to see their own objects.
    """

    def filter_queryset(self, request, queryset, view):
        if request.user.is_staff:
            return queryset
        else:
            return queryset.filter(user=request.user)


class ProjectFilterBackend(filters.BaseFilterBackend):
    """
    Filter object on project, null for project with no project.
    """

    def filter_queryset(self, request, queryset, view):
        project = request.query_params.get('project', None)
        if project is not None:
            if project == 'null':
                return queryset.filter(project__isnull=True)
            else:
                try:
                    return queryset.filter(project=int(project))
                except ValueError:
                    return queryset
        else:
            return queryset


class UserFilterBackend(filters.BaseFilterBackend):
    """
    Filter object on user, only available for staff.
    """

    def filter_queryset(self, request, queryset, view):
        if(request.user.is_staff):
            userid = request.query_params.get('user', None)
            if userid is not None:
                try:
                    userid = int(userid)
                except ValueError:
                    userid = None
            if userid is not None:
                return queryset.filter(user=userid)

        return queryset


class DateFilterBackend(filters.BaseFilterBackend):
    """
    Filter on date.
    """

    def filter_queryset(self, request, queryset, view):
        mindate = request.query_params.get('mindate', None)
        maxdate = request.query_params.get('maxdate', None)
        query = queryset
        try:
            if mindate is not None:
                mindate = dateutil.parser.parse(mindate)
                query = query.filter(start_date__gte=mindate)
            if maxdate is not None:
                maxdate = dateutil.parser.parse(maxdate)
                query = query.filter(end_date__lte=maxdate)
        except dateutil.parser.ParserError:
            raise ParseError(detail="Wrong date format")
        return query


class SupplyViewSet(viewsets.ModelViewSet):
    queryset = Supply.objects.all()
    serializer_class = SupplySerializer
    permission_classes = (IsAdminOrReadOnly,)

    @action(methods=['get'], detail=False)
    def units(self, request):
        """
        Return the supply units
        """
        return Response(dict((x, y) for x, y in Supply.UNITS),
                status=status.HTTP_200_OK)


class SupplyUsageViewSet(viewsets.ModelViewSet):
    queryset = SupplyUsage.objects.all()
    serializer_class = SupplyUsageSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        resa = get_object_or_404(Reservation.objects, pk=self.kwargs['resa_pk'])
        if not self.request.user.is_staff and self.request.user != resa.user:
            raise PermissionDenied("Your are not the owner of this reservation")
        return self.queryset.filter(reservation=resa)

    def create(self, request, *args, **kwargs):
        """
        Overload create method for auto completing based on reservation
        """
        if(isinstance(request.data, QueryDict)):
            data = request.data.dict()
        else:
            data = dict(request.data)
        try:
            resa = Reservation.objects.get(pk=self.kwargs['resa_pk'])
            if not request.user.is_staff and request.user != resa.user:
                raise PermissionDenied("Your are not the owner of this reservation")
        except Reservation.DoesNotExist:
            raise PermissionDenied("Your are not the owner of this reservation")
        if resa.status != Reservation.ACCEPTED:
            raise PermissionDenied("You can only add supply usage to an accepted reservation")

        data['reservation'] = resa.id
        if not request.user.is_staff:
            data['validated'] = False

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        """
        Overload update method in order to limit standard user actions
        """
        if(isinstance(request.data, QueryDict)):
            data = request.data.dict()
        else:
            data = dict(request.data)
        instance = self.get_object()
        if(not request.user.is_staff and instance.validated):
            raise PermissionDenied(
                "You cannot change a validated supply usage")
        if(not request.user.is_staff):
            # Prevent standard user to change the folowing values.
            data.pop('validated', None)
            data.pop('reservation', None)
        serializer = self.get_serializer(instance, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


class MachineModelViewSet(viewsets.ModelViewSet):
    queryset = MachineModel.objects.all()
    serializer_class = MachineModelSerializer
    permission_classes = (IsAdminOrReadOnly,)


class ManagerViewSet(viewsets.ModelViewSet):
    queryset = Manager.objects.all()
    serializer_class = ManagerSerializer
    permission_classes = (IsAdminOrReadOnly,)


class MachineViewSet(viewsets.ModelViewSet):
    queryset = Machine.objects.all()
    serializer_class = MachineSerializer
    permission_classes = (IsAdminOrReadOnly,)


class AvailabilityViewSet(viewsets.ModelViewSet):
    queryset = Availability.objects.all()
    serializer_class = AvailabilitySerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = [DateFilterBackend]

    def create(self, request, *args, **kwargs):
        """
        Overload create method in order to add an occurence field
        This allow to create multiple availability
        If occurence=3 create two more availabilities are created
        by adding a day between each availability
        """
        if(isinstance(request.data, QueryDict)):
            data = request.data.dict()
        else:
            data = dict(request.data)
        occurence = int(data.pop("occurence", 1))
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        if(occurence > 1):
            start_date = datetime.fromisoformat(
                request.data["start_date"])
            end_date = datetime.fromisoformat(request.data["end_date"])
            for i in range(1, occurence):
                data["start_date"] = (
                    start_date + timedelta(days=i)).isoformat()
                data["end_date"] = (end_date + timedelta(days=i)).isoformat()
                serializer = self.get_serializer(data=data)
                serializer.is_valid(raise_exception=True)
                self.perform_create(serializer)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class ReservationTypeViewSet(viewsets.ModelViewSet):
    queryset = ReservationType.objects.all()
    serializer_class = ReservationTypeSerializer
    permission_classes = (IsAdminOrReadOnly,)


class TrainingLevelView(APIView):
    """
    Retrieve, update training level for a particular user.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, user_pk, format=None):
        if(not request.user.is_staff and user_pk != request.user.id):
            raise PermissionDenied("You are not allowed to perform this action")
        tls = TrainingLevel.objects.filter(user=user_pk)
        serializer = TrainingLevelSerializer(tls, many=True)
        return Response(serializer.data)

    def put(self, request, user_pk, format=None):
        if(not request.user.is_staff):
            raise PermissionDenied("You are not allowed to perform this action")

        tls = TrainingLevel.objects.filter(user=user_pk)
        serializer = TrainingLevelSerializer(instance=tls, data=request.data, many=True)
        serializer.is_valid()
        serializer.save()
        return Response(serializer.data)


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = [DateFilterBackend]


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all().select_related('user')
    serializer_class = ReservationSerializer
    filter_backends = [DateFilterBackend, UserFilterBackend]

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [AllowAny]
        elif self.action in ['create', 'update', 'partial_update', 'retrieve']:
            permission_classes = [IsAdminOrIsSelf, IsAuthenticated]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action == "list":
            return ReservationPublicSerializer
        else:
            return ReservationSerializer

    def send_notif(self, reservation, user):
        """
        Send notification mail to the given user
        """
        status = str(OrderedDict(Reservation.STATUS)[reservation.status])
        resaname = str(reservation.reservation_type.name)
        startdate = reservation.start_date.strftime("%d/%m/%Y %H:%M:%S")
        context = {"status": status, "resaname": resaname, "startdate": startdate}
        subject = render_to_string(
            template_name='emails/updateresa_subject.txt',
            context=context
        ).strip()
        text_content = render_to_string(
            template_name='emails/updateresa_content.txt',
            context=context
        )
        html_content = render_to_string(
            template_name='emails/updateresa_content.html',
            context=context
        )
        msg = EmailMultiAlternatives(subject, text_content, email.utils.formataddr((settings.LABNAME, settings.EMAIL_SENDER)), [email.utils.formataddr((user.first_name + ' ' + user.last_name, user.email))])
        msg.attach_alternative(html_content, "text/html")
        # print(msg.message())
        try:
            msg.send()
        except:
            print("fail to send notif to " + user.email)

    def send_admin_notif(self, reservation, user):
        """
        Send notification mail for the given user
        """
        status = OrderedDict(Reservation.STATUS)[reservation.status]
        resaname = reservation.reservation_type.name
        fullusername = str(reservation.user)
        startdate = reservation.start_date.strftime("%d/%m/%Y %H:%M:%S")
        enddate = reservation.end_date.strftime("%d/%m/%Y %H:%M:%S")
        context = {"status": status, "resaname": resaname, "startdate": startdate, "enddate": enddate, "fullusername": fullusername, "commentary": str(reservation.commentary)}
        subject = render_to_string(
            template_name='emails/newresa_subject.txt',
            context=context
        ).strip()
        text_content = render_to_string(
            template_name='emails/newresa_content.txt',
            context=context
        )
        html_content = render_to_string(
            template_name='emails/newresa_content.html',
            context=context
        )
        msg = EmailMultiAlternatives(subject, text_content, email.utils.formataddr((settings.LABNAME, settings.EMAIL_SENDER)), settings.EMAIL_ADMIN, reply_to=[email.utils.formataddr((user.first_name + ' ' + user.last_name, user.email))])
        msg.attach_alternative(html_content, "text/html")
        # print(msg.message())
        try:
            msg.send()
        except:
            print("fail to send notif to " + user.email)

    def create(self, request, *args, **kwargs):
        """
        If it's a standard user check the charter and the training level
        """
        if(not request.user.is_staff):
            if(not request.user.charter):
                raise serializers.ValidationError(
                    "You must agree with the charter before making any reservation", code="invalid")
            if('status' in request.data):
                raise PermissionDenied(
                    "You are not allowed to specify the status")
            rtype = ReservationType.objects.get(pk=request.data['reservation_type'])
            if not rtype.need_manager:
                for model in rtype.needs.all():
                    tl = TrainingLevel.objects.get(machine_model=model, user=request.user)
                    if tl.need_manager:
                        raise serializers.ValidationError(
                            "You need a manager for this machine, choose an initiation", code="invalid")

        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        # if non admin set user to current user and send notifications
        if(not self.request.user.is_staff):
            instance = serializer.save(user=self.request.user)
            self.send_admin_notif(instance, self.request.user)
            self.send_notif(instance, self.request.user)
        else:
            serializer.save()

    def update(self, request, *args, **kwargs):
        """
        Forbid the change of a reservation which is not in Requested mode
        Send a notification mail to the owner if the status change
        """
        instance = self.get_object()
        if(not request.user.is_staff):
            if(instance.status != Reservation.REQUESTED):
                raise PermissionDenied(
                    "You cannot change a validated reservation")
        partial = kwargs.pop('partial', False)
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial, context={'request': request})
        serializer.is_valid(raise_exception=True)
        status_dict = OrderedDict(Reservation.STATUS)
        # check changing status before performing the change
        statuschanged = request.data['status'] != status_dict[instance.status]
        self.perform_update(serializer)
        if(statuschanged):
            self.send_notif(instance, instance.user)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


class RefreshResourcesView(APIView):
    #permission_classes = [IsAdminUser]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        staticdir = settings.STATIC_ROOT
        if not staticdir:  # devmod
            staticdir = settings.STATICFILES_DIRS[0]
        f = open(staticdir + "/resources.min.json", "w")
        ress = {'machines': MachineSerializer(Machine.objects.all(), many=True).data,
                'managers': ManagerSerializer(Manager.objects.all(), many=True).data,
                }
        f.write(json.dumps(ress))
        f.close()
        ress['reservation_types'] = ReservationTypeSerializer(ReservationType.objects.all(), many=True).data
        ress['machine_models'] = MachineModelSerializer(MachineModel.objects.all(), many=True).data
        ress['supplies'] = SupplySerializer(Supply.objects.all(), many=True).data
        f = open(staticdir + "/resources.json", "w")
        f.write(json.dumps(ress))
        f.close()
        return Response(ress)


class UsagesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):

        statusD = {v: i for i, v in Reservation.STATUS}

        queryset = Reservation.objects

        project = request.query_params.get('project', None)
        if project is not None:
            if project == 'null':
                queryset = queryset.filter(project__isnull=True)
            else:
                try:
                    queryset = queryset.filter(project=int(project))
                except ValueError:
                    raise ParseError(detail="Wrong project id format")

        mindate = request.query_params.get('mindate', None)
        maxdate = request.query_params.get('maxdate', None)
        queryset = queryset
        try:
            if mindate is not None:
                mindate = dateutil.parser.parse(mindate)
                queryset = queryset.filter(start_date__gte=mindate)
            if maxdate is not None:
                maxdate = dateutil.parser.parse(maxdate)
                queryset = queryset.filter(end_date__lte=maxdate)
        except:
            raise ParseError(detail="Wrong date format")

        if(request.user.is_staff):
            user = request.query_params.get('user', None)
            if user is not None:
                try:
                    queryset = queryset.filter(user=int(user))
                except:
                    raise ParseError(detail="Wrong user id format")
        else:
            queryset = queryset.filter(user=request.user)

        resatype = request.query_params.get('type', None)
        if resatype is not None:
            try:
                queryset = queryset.filter(reservation_type=int(resatype))
            except:
                raise ParseError(detail="Wrong type id format")

        status = request.query_params.get('status', None)
        if status is not None:
            try:
                queryset = queryset.filter(status=statusD[status])
            except:
                raise ParseError(detail="Wrong status format")

        sup_queryset = SupplyUsage.objects.all()
        validated = request.query_params.get('validated', None)
        if validated is not None:
            try:
                sup_queryset = sup_queryset.filter(validated=validated == "true")
            except:
                raise ParseError(detail="Wrong validated format")

        queryset = queryset.defer('commentary', 'created_date', 'uses', 'manager')
        queryset = queryset.prefetch_related(Prefetch('reservation_type', queryset=ReservationType.objects.only('name')))
        queryset = queryset.prefetch_related(Prefetch('user', queryset=get_user_model().objects.only('first_name', 'last_name', 'username')))
        queryset = queryset.prefetch_related(Prefetch('project', queryset=Project.objects.only('name')))
        queryset = queryset.prefetch_related(Prefetch('supplies', queryset=sup_queryset))
        queryset = queryset.prefetch_related(Prefetch('supplies__supply', queryset=Supply.objects.only('name', 'unit')))

        resas = {}
        supplies = {}
        users = {}
        projects = {}

        units = dict(Supply.UNITS)

        for resa in queryset:
            if resa.reservation_type.id not in resas:
                resas[resa.reservation_type.id] = {'name': resa.reservation_type.name, 'total': 0, 'usages': {}}
            rtype = resas[resa.reservation_type.id]
            resadata = ReservationUsageSerializer(resa, context={'request': request}).data
            rtype['usages'][resa.id] = resadata
            rtype['total'] += resadata['duration']
            for supply_usage in resa.supplies.all():
                if supply_usage.supply.id not in supplies:
                    supplies[supply_usage.supply.id] = {'name': supply_usage.supply.name, 'unit': units[supply_usage.supply.unit], 'total': 0, 'usages': []}
                data = SupplyUsageSerializer(supply_usage).data
                supplies[supply_usage.supply.id]['usages'].append(data)
                supplies[supply_usage.supply.id]['total'] += supply_usage.quantity
            if resa.user.id not in users:
                users[resa.user.id] = {'first_name': resa.user.first_name, 'last_name': resa.user.last_name, 'username': resa.user.username}
            if resa.project and resa.project.id not in projects:
                projects[resa.project.id] = {'name': resa.project.name}

        #from django.db import connection
        # for q in connection.queries:
        #    print(q['sql'])
        #    print()

        return Response({'reservations': resas, 'supplies': supplies, 'users': users, 'projects': projects})


# Add an ical view if django-cal is installed
if 'django_ical' in settings.INSTALLED_APPS:
    from django_ical.views import ICalFeed

    class ReservationsCal(ICalFeed):
        """
        A simple event calender
        """
        product_id = '-//' + settings.LABNAME + '//FR'
        timezone = settings.TIME_ZONE
        file_name = "event.ics"

        def items(self):
            now = timezone.now()
            wd = now.weekday()
            monday = (now - timedelta(days=wd)).replace(hour=0, minute=0, second=0)
            resas = Reservation.objects.filter(date__gte=monday)
            events = Event.objects.filter(start_date__gte=monday)
            return (list(resas) + list(events))

        def item_guid(self, item):
            if isinstance(item, Event):
                return 'e' + str(item.id)
            else:
                return 'r' + str(item.id)

        def item_title(self, item):
            if isinstance(item, Event):
                return item.name
            else:
                return item.reservation_type.name

        def item_link(self, item):
            return '/'

        def item_description(self, item):
            if isinstance(item, Event):
                return item.description
            else:
                return item.commentary

        def item_start_datetime(self, item):
            return item.start_date

        def item_end_datetime(self, item):
            return item.end_date
