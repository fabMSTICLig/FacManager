"""
Copyright (C) 2020-2022 LIG Université Grenoble Alpes


This file is part of FacManager.

FacManager is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

FacManager is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with FacManager. If not, see <https://www.gnu.org/licenses/>

@author Germain Lemasson
"""

from rest_framework import serializers, exceptions
from django.contrib.auth import get_user_model, authenticate
from .models import Organization, Project


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer class of the User Model

    The class member person is a nested representation
    """
    externe = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'is_staff', 'externe', 'charter', 'organizations', 'projects', 'reservations','rgpd_accept')
        read_only_fields = ('username',)

    def get_externe(self, obj):
        """
        Field function that return true if the user as no password
        if so the user is using CAS for authentification
        """
        return len(obj.password)==0

class UserPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'first_name', 'last_name',)
        read_only_fields = ('username', 'first_name', 'last_name',)


class PasswordSerializer(serializers.Serializer):
    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

class LoginSerializer(serializers.Serializer):
    """
    This serializer defines two fields for authentication:
      * username
      * password.
    It will try to authenticate the user with when validated.
    """
    username = serializers.CharField(
        label="Username",
        write_only=True
    )
    password = serializers.CharField(
        label="Password",
        # This will be used when the DRF browsable API is enabled
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )

    def validate(self, attrs):
        # Take username and password from request
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            # Try to authenticate the user using Django auth framework.
            user = authenticate(request=self.context.get('request'),
                                username=username, password=password)
            if not user:
                # If we don't have a regular user, raise a ValidationError
                msg = 'Access denied: wrong username or password.'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'Both "username" and "password" are required.'
            raise serializers.ValidationError(msg, code='authorization')
        # We have a valid user, put it in the serializer's validated_data.
        # It will be used in the view.
        attrs['user'] = user
        return attrs

class NewUserSerializer(serializers.Serializer):
    """
    Serializer for create new user endpoint.
    """
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ['id', 'name', 'contact', 'type']


class OrganizationPublicSerializer(OrganizationSerializer):
    class Meta:
        model = Organization
        fields = ['id', 'name', 'type']
        readonly = ['id', 'name', 'type']


class ProjectSerializer(serializers.ModelSerializer):
    """
    Serializer for project

    """
    class Meta:
        model = Project
        fields = '__all__'
