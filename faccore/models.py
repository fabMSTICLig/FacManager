"""
Copyright (C) 2020-2022 LIG Université Grenoble Alpes


This file is part of FacManager.

FacManager is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

FacManager is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with FacManager. If not, see <https://www.gnu.org/licenses/>

@author Germain Lemasson
"""

from django.db import models
from django.core.validators import MinValueValidator
from django.conf import settings
from facusers.models import Project


class NamedModel(models.Model):
    """An abstract class used for model with a name """

    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class MachineModel(NamedModel):
    """
    Represent a model of machine
    ----------
    name : str
        Name of the model
    description : str, optional
        Description of the model
    user_levels : [TrainingLevel]
        TrainingLevel for each model and each user

    """

    description = models.CharField(max_length=300, null=True, blank=True)
    display_order = models.PositiveIntegerField(default=0)
    user_levels = models.ManyToManyField(
        settings.AUTH_USER_MODEL, blank=True, through='TrainingLevel',
        related_name='training_levels')


class TrainingLevel(models.Model):
    machine_model = models.ForeignKey(MachineModel, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    level = models.PositiveIntegerField(default=0)
    need_manager = models.BooleanField(default=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['machine_model', 'user'],
                name='One training level per user/machine')
        ]


class Supply(NamedModel):
    """
    Represent a supply for machine (PLA, wood, ...)
    ----------
    name : str
    unit : int
    description : str, optional
    categories : [MachineCategory]
        Categories of machine using this supply
    unit : int
        Unit for the quantifiable (m,m2,m3,kg,p)
    """

    METRE = 2
    METRESQUARE = 3
    METRECUBE = 4
    GRAMME = 5
    PIECE = 6
    UNITS = (
        (METRE, ("m")),
        (METRESQUARE, ("m2")),
        (METRECUBE, ("m3")),
        (GRAMME, ("g")),
        (PIECE, ("p")),
    )
    unit = models.SmallIntegerField(choices=UNITS, default=GRAMME)

    description = models.CharField(max_length=300, null=True, blank=True)
    models = models.ManyToManyField(MachineModel, blank=True)

    def __str__(self):
        return self.name


class ReservationType(NamedModel):
    """
    Represent a type of reservation
    ----------
    name : str
    needs : [MachineModel]
        Machines needed for this type of reservation
    description : str, optional
    min_time_slot : float
        minimal possible time slot for this type of reservation
    max_time_slot : float
        maximal duration of this type of reservation
    need_manager : bool
        true if this type of reservation needs a manager
    """
    needs = models.ManyToManyField(MachineModel, blank=True)
    description = models.CharField(max_length=300, null=True, blank=True)
    min_time_slot = models.DecimalField(
        max_digits=10, decimal_places=3, default=0.5,
        validators=[MinValueValidator(0.0)])
    max_time_slot = models.DecimalField(
        max_digits=10, decimal_places=3, default=1,
        validators=[MinValueValidator(0.0)])
    need_manager = models.BooleanField(default=False)


class TimedResource(models.Model):
    """
    Base class for Resource that can be reserved for some time
    """

    def __str__(self):
        return self.getChild().__str__()

    def getChild(self):
        try:
            return self.machine
        except (Machine.DoesNotExist):
            return self.manager


class Availability(models.Model):
    """
    Represent an availability
    ----------
    start_date : date
    end_date : date
    resources : [TimedResource]
        Resources available for this amount of time
    """
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    resources = models.ManyToManyField(TimedResource)

    def __str__(self):
        return (str(self.resources) + '(' +
                self.start_date.strftime("%Y-%m-%d") +
                ' ' + self.end_date.strftime("%Y-%m-%d") + ')')


class Machine(NamedModel, TimedResource):
    """
    Represent a particlar machine
    ----------
    name : str
    model : MachineModel
        The model of this machine
    """
    model = models.ForeignKey(
        MachineModel, on_delete=models.CASCADE, related_name='instances')

    def __str__(self):
        return str(self.model) + ' ' + self.name


class Manager(NamedModel, TimedResource):
    """
    Represent a Manager wich is a resource
    ----------
    name : str
    email : email
    """
    email = models.EmailField(max_length=100, null=True, blank=True)


class Reservation(models.Model):
    """
    Represent a reservation
    ----------
    user : settings.AUTH_USER_MODEL
        user making this reservation
    project : Project, optional
        Project in which the reservation is took
        date : datetime
        Starting date and time of this reservation
    end_date : datetime
        Ending date and time of this reservation
    status : int
        Status of this reservation can be (Requested,Accepted,Denied,Changed)
    reservation_type : ReservationType
        Type of this reservation
    uses : [Machine], optional
        Machines used for this reservation
        (verified with the need of the reservation_type)
    manager : Manager, optional
        Manager used for this reservation
    created_date : datetime
        Time of creation of this reservation
    commentary : string, optional
        Commentary used by user And Admin to communicate

    """
    REQUESTED = 1
    ACCEPTED = 2
    DENIED = 3
    CHANGED = 4
    STATUS = (
        (REQUESTED, ("Requested")),
        (ACCEPTED, ("Accepted")),
        (DENIED, ("Denied")),
        (CHANGED, ("Changed")),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name='reservations')
    project = models.ForeignKey(
        Project, null=True, blank=True, on_delete=models.SET_NULL)
    start_date = models.DateTimeField()

    status = models.SmallIntegerField(choices=STATUS, default=REQUESTED)
    end_date = models.DateTimeField()
    reservation_type = models.ForeignKey(
        ReservationType, on_delete=models.CASCADE)
    uses = models.ManyToManyField(Machine, blank=True)
    manager = models.ForeignKey(
        Manager, on_delete=models.SET_NULL, blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    commentary = models.CharField(max_length=300, null=True, blank=True)

    def __str__(self):
        return (str(self.user) +
                '(' + str(self.start_date) +
                ' ' + str(self.end_date) + ')')


class SupplyUsage(models.Model):
    """
    Represent the usage of supplies
    ----------
    reservation : Reservation
        the attached reservation
    quantity : float
    supply : Supply
        Type of supply used
    validated : bool
        True if this usage is validated by an admin
    """
    reservation = models.ForeignKey(
        Reservation, on_delete=models.CASCADE, related_name='supplies')
    quantity = models.DecimalField(max_digits=10, decimal_places=3)
    supply = models.ForeignKey(
        Supply, on_delete=models.PROTECT, related_name='usages')
    validated = models.BooleanField(default=False)

    def __str__(self):
        units = dict(Supply.UNITS)
        return (str(self.supply) +
                ' ' + str(self.quantity) +
                ' ' + units[self.supply.unit])


class Event(NamedModel):
    """
    Represent an event (Fablab closed, Visit)
    start_date : datetime
        Starting date and time of this event
    end_date : datetime
        Ending date and time of this event
    description : str, optional
    """

    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    description = models.CharField(max_length=300, null=True, blank=True)
