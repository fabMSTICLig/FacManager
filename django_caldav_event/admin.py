from cryptography.fernet import Fernet
import base64
from django.contrib import admin
from django.forms import ModelForm, PasswordInput
from django import forms
from .app_settings import app_settings
from .models import CalendarInfos, CalDavEvent

class CalendarInfosForm(forms.ModelForm):
    new_password = forms.CharField(required=False,widget=forms.PasswordInput()) 
    
    class Meta:
        model = CalendarInfos
        exclude = ['password_hash']


# Register your models here.
@admin.register(CalendarInfos)
class CalendarInfosAdmin(admin.ModelAdmin):
    form = CalendarInfosForm
    fieldsets = (
        (None, {
            'fields': ('name', 'login', 'new_password', 'url',),
        }),
    )

    def save_model(self, request, obj, form, change):
        if(form.cleaned_data['new_password']):
            f = Fernet(app_settings.CIPHER_KEY)
            passw = f.encrypt(base64.b64encode(bytes(form.cleaned_data['new_password'], 'ascii')))
            obj.password_hash = passw.decode('ascii')
            obj.save()
        else:
            obj.save()
@admin.register(CalDavEvent)
class CalDavEventAdmin(admin.ModelAdmin):
    pass

