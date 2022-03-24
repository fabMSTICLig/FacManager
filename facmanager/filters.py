"""
Copyright (C) 2020-2022 LIG Université Grenoble Alpes


This file is part of FacManager.

FacManager is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

FacManager is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with FacManager. If not, see <https://www.gnu.org/licenses/>

@author Germain Lemasson
"""

from rest_framework import filters


class IdsFilter(filters.BaseFilterBackend):
    """
    Filter against entity
    """

    def filter_queryset(self, request, queryset, view):
        if('ids' in request.query_params.keys()):
            ids_q = request.query_params.get('ids', None)
            if(ids_q is not None and ids_q != ""):
                try:
                    return queryset.filter(pk__in=[int(v) for v in ids_q.split(',')]).distinct()
                except ValueError:
                    return queryset.none()
            else:
                return queryset.none()
        else:
            return queryset
