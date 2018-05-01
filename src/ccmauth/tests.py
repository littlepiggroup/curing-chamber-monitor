# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from unittest import TestCase

from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from django.contrib.auth import get_user_model


class UserApiTests(APITestCase):

    def test_create_user(self):
        self._force_authenticate()
        user_model = get_user_model()
        req_body = {user_model.USERNAME_FIELD: "13482788878", "password": "123456", "is_active": True}
        url = reverse('ccm_user-list')
        resp = self.client.post(url, req_body, format='json')
        self.assertEqual(status.HTTP_201_CREATED, resp.status_code)

    def test_me(self):
        self._force_authenticate()
        url = reverse('ccm_user-me')
        resp = self.client.get(url, format='json')
        self.assertEqual(status.HTTP_200_OK, resp.status_code)

    def test_partial_update_me(self):
        self._force_authenticate()
        user_model = get_user_model()
        url = reverse('ccm_user-me')
        req_body = {user_model.USERNAME_FIELD: "13482787778", "first_name": "lll"}
        resp = self.client.patch(url, req_body, format='json')
        self.assertEqual(status.HTTP_200_OK, resp.status_code)
        key = {user_model.USERNAME_FIELD: "13482787778"}
        user = user_model.objects.get(**key)
        self.assertEqual("lll", user.first_name)

    def _force_authenticate(self):
        user_model = get_user_model()
        # create an user using user model directly
        user = user_model(password="123456", is_active=True, is_superuser=True)
        setattr(user, user_model.USERNAME_FIELD, "13482777788")
        user.save()
        # force authenticate via created user
        key = {user_model.USERNAME_FIELD: "13482777788"}
        user = user_model.objects.get(**key)
        self.client.force_authenticate(user=user)


class UserModelTest(TestCase):
    def test_user_db(self):
        user_model = get_user_model()
        user = user_model(password="123456", is_active=True)
        setattr(user, user_model.USERNAME_FIELD, "13482787778")
        user.save()
        old_count = user_model.objects.values('id').count()
        new_user = user_model(password="123456", is_active=True)
        setattr(new_user, user_model.USERNAME_FIELD, "13482787779")
        new_user.save()
        new_count = user_model.objects.values('id').count()
        self.assertNotEqual(old_count, new_count)
