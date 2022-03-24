"""
Copyright (C) 2020-2022 LIG Université Grenoble Alpes


This file is part of FacManager.

FacManager is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

FacManager is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with FacManager. If not, see <https://www.gnu.org/licenses/>

@author Germain Lemasson
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Organization, Project

class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('FacManager', {'fields': ('rgpd_accept','organizations',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('FacManager', {'fields': ('rgpd_accept','organizations',)}),
    )
    change_form_template = "admin/auth/user/change_form.html"
    change_list_template = "admin/auth/user/change_list.html"
admin.site.register(User, CustomUserAdmin)

@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    search_fields = ('name',)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    filter_horizontal = ('members',)
