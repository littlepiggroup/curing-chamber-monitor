# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.hashers import make_password
from rest_framework import serializers, exceptions
from rest_framework.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        exclude = ('is_superuser', )
        extra_kwargs = {'password': {'write_only': True}, 'date_joined': {'read_only': True}}

    def create(self, validated_data):
        raw_password = validated_data["password"]
        validated_data["password"] = make_password(raw_password)
        user = super(UserSerializer, self).create(validated_data)
        user._password = raw_password
        return user

    def update(self, instance, validated_data):
        raw_password = None
        if "password" in validated_data:
            raw_password = validated_data["password"]
            validated_data["password"] = make_password(raw_password)
        user = super(UserSerializer, self).update(instance, validated_data)
        if raw_password:
            user._password = raw_password
        return user


class UserRegisterSerializer(UserSerializer):
    class Meta:
        model = get_user_model()
        exclude = ('is_staff', 'is_superuser', 'is_active', 'groups', 'user_permissions')
        read_only_fields = ('date_joined',)
        extra_kwargs = {'password': {'write_only': True}}

    def is_valid(self, raise_exception=False):
        user_model = get_user_model()
        user = user_model(**self.initial_data)
        user.register_pre_process(self.initial_data)
        return super(UserRegisterSerializer, self).is_valid(raise_exception)

    def save(self, **kwargs):
        instance = super(UserRegisterSerializer, self).save(**kwargs)
        instance.register_post_process()
        return instance

    def update(self, instance, validated_data):
        pass


class UserPasswordResetSerializer(UserSerializer):
    class Meta:
        model = get_user_model()
        fields = (get_user_model().USERNAME_FIELD, 'password')

    def is_valid(self, raise_exception=False):
        err = None
        user_model = get_user_model()
        login_name = self.initial_data.get(user_model.USERNAME_FIELD)
        if login_name:
            key = {user_model.USERNAME_FIELD: login_name}
            try:
                user = user_model.objects.get(**key)
                if not user.is_active:
                    err = ValidationError({'detail': _('User account disabled.')})
                else:
                    user.password_reset_pre_process(self.initial_data)
                    password = self.initial_data.get('password')
                    new_password = self.initial_data.get('new_password')
                    if password and new_password:
                        if password == new_password:
                            err = ValidationError({'detail': _('The new password is same as before.')})
                        elif not user.password_reset_password_check(password):
                            err = exceptions.AuthenticationFailed()
                        else:
                            self.password_reset_user = user
                    else:
                        err = ValidationError({'detail': _("Must include '%s', '%s' and '%s'." %
                                                                    (user_model.USERNAME_FIELD,  'password',
                                                                     'new_password'))})
            except user_model.DoesNotExist:
                err = ValidationError({'detail': _('User is not existed.')})
        else:
            err = exceptions.NotAuthenticated({'detail': _("Must include '%s', '%s' and '%s'." %
                                                           (user_model.USERNAME_FIELD, 'password', 'new_password'))})

        if err and raise_exception:
            raise err

        return not err

    def save(self, **kwargs):
        self.password_reset_user.set_password(self.initial_data["new_password"])
        self.password_reset_user.save()
        # because password_reset_user.save() will set _password to None
        # call pass _password(raw_password) again to reset _password
        self.password_reset_user.set_password(self.initial_data["new_password"])
        self.password_reset_user.password_reset_post_process()

    def update(self, instance, validated_data):
        pass


class UserLoginSerializer(UserSerializer):
    class Meta:
        model = get_user_model()
        fields = (get_user_model().USERNAME_FIELD, 'password')
        read_only_fields = (get_user_model().USERNAME_FIELD, 'password')

    def is_valid(self, raise_exception=False):
        err = None
        user_model = get_user_model()
        login_name = self.initial_data.get(user_model.USERNAME_FIELD)
        password = self.initial_data.get('password')
        if login_name and password:
            user = authenticate(**self.initial_data)
            if user:
                if not user.is_active:
                    err = exceptions.AuthenticationFailed({'detail': _('User account disabled.')})
                else:
                    self.authencated_user = user
            else:
                raise exceptions.AuthenticationFailed()
        else:
            err = exceptions.NotAuthenticated({'detail': _("Must include '%s', '%s' and '%s'." %
                                                           (user_model.USERNAME_FIELD, 'password', 'new_password'))})

        if err and raise_exception:
            raise err

        return not err

    def save(self, **kwargs):
        pass

    def update(self, instance, validated_data):
        pass


class UserDetailSerializer(UserSerializer):
    class Meta:
        model = get_user_model()
        exclude = ('is_staff', 'is_superuser', 'is_active', 'password')
        read_only_fields = ('date_joined', )
