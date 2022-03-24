"""
Copyright (C) 2020-2022 LIG Université Grenoble Alpes


This file is part of FacManager.

FacManager is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

FacManager is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with FacManager. If not, see <https://www.gnu.org/licenses/>

@author Germain Lemasson
"""

from django.dispatch import receiver
from django_cas_ng.signals import cas_user_authenticated
from django.conf import settings

try:
    from django_auth_ldap.backend import LDAPBackend
    @receiver(cas_user_authenticated)
    def cas_user_authenticated_callback(sender, **kwargs):
        args = {}
        args.update(kwargs)
        if (hasattr(settings,'AUTH_LDAP_USER_SEARCH')):
            user = LDAPBackend().populate_user(args.get('user').username)
            if user is not None:
                user.save()
except ImportError as e:
    pass  # module doesn't exist, deal with it.
