# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import time
import unittest

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Project, BuildingCompany, ProjectName, Camera, EzvizAccount, Video


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

    def test_ezviz(self):
        # Create ezviz account
        url = reverse('ezviz_account-list')
        data = {"user_name":"ezviz_name", "app_key":"app_key_value", "secret":"secreet_value"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.get(url)
        ezviz_account = response.data['results'][0]
        self.assertEqual('ezviz_name', ezviz_account['user_name'])

        # Create project
        building_company = BuildingCompany(name="test_company")
        building_company.save()
        url = reverse('project-list')
        data = {'names': [{"name": 'testname1'}, {"name": "testname2"}], 'building_company': building_company.id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Create camera
        url = reverse('camera-list')
        data = {'ezviz_account': 1, 'project': 1,
                'device_serial_number': '123456', 'rtmp_address':'rtmp://xxx'}
        response = self.client.post(url, data, format='json')
        # print response.data
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @unittest.skip("Need run manually. And setup camera before.")
    def test_add_camera(self):

        # user input: device_number, ezviz user/name password.
        building_company = BuildingCompany(name="test_company")
        building_company.save()
        new_project = Project(building_company_id=building_company.id)
        new_project.save()
        ezviz_account = EzvizAccount(user_name='13788889999', app_key="app_key_val", secret="secret_val")
        ezviz_account.save()
        camera = Camera(ezviz_account=ezviz_account, project = new_project, device_serial_number="762881292",
                        rtmp_address='rtmp://rtmp.open.ys7.com/openlive/bfed2855f58d4dd6891e670060540a7a')
        camera.save()
        new_cameras = Camera.objects.all()
        self.assertEqual('762881292', new_cameras[0].device_serial_number)
        self.assertEqual('rtmp://rtmp.open.ys7.com/openlive/bfed2855f58d4dd6891e670060540a7a',
                         new_cameras[0].rtmp_address)
        self.assertEqual(1, new_cameras[0].project.id)

        from ccm.ccmapp.videomgr import videomgr
        videomgr.collect()
        videos = Video.objects.all()
        self.assertEqual(1, len(videos))
        video = videos[0]
        self.assertTrue(video.url_path.find('static/videos/1-762881292') == 0)


    def test_upload_video(self):
        # TODO
        pass

    def test_month_project_report(self):
        # TODO.
        pass

