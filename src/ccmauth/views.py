# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth import (login as django_login, logout as django_logout)
from rest_framework import viewsets, status
from rest_framework.generics import CreateAPIView, GenericAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from ccmauth.permissions import UsersAdminPermissions
from ccmauth.serializers import UserSerializer, UserRegisterSerializer, UserLoginSerializer, \
    UserPasswordResetSerializer, UserDetailSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = (UsersAdminPermissions, )

    filter_fields = ('id', get_user_model().USERNAME_FIELD, 'first_name', 'last_name', 'is_active', 'is_staff',
                     'date_joined', 'last_login')
    ordering_fields = ('id', get_user_model().USERNAME_FIELD, 'first_name', 'last_name', 'is_active', 'is_staff',
                       'date_joined', 'last_login')


class RegisterView(CreateAPIView):
    serializer_class = UserRegisterSerializer
    permission_classes = (AllowAny,)


class PasswordResetView(GenericAPIView):
    serializer_class = UserPasswordResetSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        # Create a serializer with request.data
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        # Return the success message with OK HTTP status
        return Response(status=status.HTTP_200_OK)


class LoginView(GenericAPIView):
    serializer_class = UserLoginSerializer
    permission_classes = (AllowAny, )

    def login(self, request, user):
        django_login(request, user)
        return Response(status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=self.request.data, context={'request': request})
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            return Response(data={'detail': e.detail}, status=status.HTTP_401_UNAUTHORIZED)

        return self.login(request, serializer.authencated_user)


class LogoutView(APIView):
    permission_classes = (AllowAny, )

    def logout(self, request):
        django_logout(request)
        return Response(status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        return self.logout(request)

    def get(self, request, *args, **kwargs):
        if getattr(settings, 'ACCOUNT_LOGOUT_ON_GET', False):
            response = self.logout(request)
        else:
            response = self.http_method_not_allowed(request, *args, **kwargs)
        return self.finalize_response(request, response, *args, **kwargs)


class UserMeView(UpdateAPIView):
    queryset = get_user_model().objects.filter(is_active=True)
    serializer_class = UserDetailSerializer

    def get(self, request, format=None):
        return Response(self.serializer_class(request.user).data)

    def put(self, request, *args, **kwargs):
        self.kwargs['pk'] = request.user.id
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        self.kwargs['pk'] = request.user.id
        return self.partial_update(request, *args, **kwargs)

