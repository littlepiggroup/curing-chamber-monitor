# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import time
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Project, BuildingCompany, ProjectName


# Create your tests here.
#HowTO: https://scotch.io/tutorials/build-a-rest-api-with-django-a-test-driven-approach-part-1

# Test db behavior
class ProjectTest(TestCase):
    def test_project_db(self):
        building_company = BuildingCompany(name="test_company")
        building_company.save()
        old_count = Project.objects.values('id').count()
        new_project = Project(building_company_id=building_company.id)
        new_project.save()
        new_count = Project.objects.values('id').count()
        self.assertNotEqual(old_count, new_count)


# Test API behavior
class ProjectApiTests(APITestCase):
    def test_create_project(self):
        """
        Ensure we can create a new project object.
        """
        building_company = BuildingCompany(name="test_company")
        building_company.save()
        url = reverse('project-list')
        data = {'names': [{"name": 'testname1'}, {"name": "testname2"}], 'building_company': building_company.id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['building_company'], data['building_company'])
        name_count = ProjectName.objects.values('id').count()
        self.assertEqual(2, name_count)

    def test_project_ordering(self):
        building_company = BuildingCompany(name="test_company")
        building_company.save()
        building_company2 = BuildingCompany(name="test_company_2")
        building_company2.save()
        url = reverse('project-list')
        data = {'names': [{"name": 'testname1'}, {"name": "testname2"}], 'building_company': building_company.id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        time.sleep(1)
        data = {'names': [{"name": 'testname3'}, {"name": "testname4"}], 'building_company': building_company2.id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        project_count = Project.objects.values('id').count()
        self.assertEqual(2, project_count)
        name_count = ProjectName.objects.values('id').count()
        self.assertEqual(4, name_count)
        response = self.client.get(url)
        self.assertEquals(building_company.id, response.data['results'][0]['building_company'])
        self.assertEquals(building_company2.id, response.data['results'][1]['building_company'])
