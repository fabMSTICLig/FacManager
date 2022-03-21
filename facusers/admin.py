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
