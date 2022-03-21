"""
Faccore module manage the usages of the fac lab


A usage can be a supply usage or tacking a reservation.
Reservations refers to activities such as using a machine,
participating to a lessons or receiving personalized support.


This module allow to manage two fac lab resources:
the managers and the machines. A reservation can uses ressources but
two reservations cannot use the same resource as the same time.
It also allow to manage the availabilities of the ressources.
A person cannot make a reservation if the needed machines are not 
available(for example a machine under reparation).

A supply usage is for example the use of machine consumable.

"""
