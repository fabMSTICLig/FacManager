"""
Copyright (C) 2020-2022 LIG Université Grenoble Alpes


This file is part of FacManager.

FacManager is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

FacManager is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with FacManager. If not, see <https://www.gnu.org/licenses/>

@author Germain Lemasson
"""

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
