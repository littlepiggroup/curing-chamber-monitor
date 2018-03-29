# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import time
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Project, Company


# Create your tests here.
#HowTO: https://scotch.io/tutorials/build-a-rest-api-with-django-a-test-driven-approach-part-1

# Test db behavior
class ProjectTest(TestCase):
    def test_project_db(self):
        old_count = Project.objects.count()
        new_company = Company(name="microsoft")
        new_company.save()
        new_project = Project(company =  new_company, name="testproj", code="hello", title = "world")
        new_project.save()
        new_count = Project.objects.count()
        self.assertNotEqual(old_count, new_count)


# Test API behavior
class ProjectApiTests(APITestCase):
    def test_create_project(self):
        """
        Ensure we can create a new project object.
        """
        new_company = Company(name="microsoft")
        new_company.save()
        url = reverse('project-list')
        data = {'name': 'testname', 'code':'another', 'company':1}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], data['name'])

    def test_project_ordering(self):
        new_company = Company(name="microsoft")
        new_company.save()
        url = reverse('project-list')
        data = {'name': 'first', 'code':'first_code', 'company':1}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        time.sleep(1)
        data = {'name': 'second', 'code':'second_code', 'company':1}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.get(url)
        self.assertEquals('second', response.data['results'][0]['name'])
