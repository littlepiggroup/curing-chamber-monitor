# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import time
import unittest

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Project, BuildingCompany, ProjectName, Camera, EzvizAccount, Video


class CcmApiTestCase(APITestCase):
    def _force_authenticate(self):
        user_model = get_user_model()
        # create an user using user model directly
        user = user_model(password="123456", is_active=True)
        setattr(user, user_model.USERNAME_FIELD, "13482777788")
        user.save()
        # force authenticate via created user
        key = {user_model.USERNAME_FIELD: "13482777788"}
        user = user_model.objects.get(**key)
        self.client.force_authenticate(user=user)


class ProjectApiTests(CcmApiTestCase):

    def test_create_company_project_api(self):
        self._force_authenticate()
        # Step 1: add building_company_users as the source to fetch data from sample website.
        req_body = {"login_name": "login_name_to_sample_website"}
        url = reverse('building_company_user-list')
        resp = self.client.post(url, req_body, format='json')
        self.assertEqual(status.HTTP_201_CREATED, resp.status_code)

        # Step 2: create building company with name
        req_body = {'name': 'microsoft'}
        url = reverse('building_company-list')
        resp = self.client.post(url, req_body, format='json')
        self.assertEqual(status.HTTP_201_CREATED, resp.status_code)

        # Step 3: add projects (identified by names) to building company.
        url = reverse('project-list')
        req_body = {'names': [{"name": 'CenturyParkProject'}, {"name": "ShiJiGongYuanProject"}], 'building_company': 1}
        resp = self.client.post(url, req_body, format='json')
        self.assertEqual(status.HTTP_201_CREATED, resp.status_code)
        self.assertEqual(resp.data['building_company'], req_body['building_company'])
        name_count = ProjectName.objects.values('id').count()
        self.assertEqual(2, name_count)

        # Note: after these operations, there will be crontab task to run samplemgr.update_samples.Sync.sync to
        # fetch the sample data from sample website. And you can also run manually, python manage.py syc_samples to
        # fetch data.

    def test_video_related_api(self):
        # Prepare data
        self.test_create_company_project_api()

        # All data in req_body are from a given ezviz account.
        req_body = {"user_name": "13788889999", 'app_key': 'app_key_val', 'secret': 'secret_val'}
        url = reverse('ezviz_account-list')
        resp = self.client.post(url, req_body, format='json')
        self.assertEqual(status.HTTP_201_CREATED, resp.status_code)

        # TODO: for now, rtmp_address is mandatory. In future, it should be fetched automatically.
        # TODO: The rtmp address is also got from ezviz website (after login and bind the camera).
        req_body = {'ezviz_account':1, 'project': 1,
                    'device_serial_number': "762881292"
        }
        url = reverse('camera-list')
        resp = self.client.post(url, req_body, format='json')
        self.assertEqual(status.HTTP_201_CREATED, resp.status_code)

        # Note: after above operations, there should be crontab to record the video at 8:00 am on everyday.
        # (TODO: record randomly (8,9,10).  And you can also run 'ptyhon manage.py collect_videos' to save video
        # for every camera. The video file will be created  ccm/ccmapp/static/videos/. And you can get at url
        # <IP>/static/videos/<video_name>.mp4. You can fetch the path 'static/videos/<video_name>.mp4' from
        # models.Video.url_path. You can filter videos via Video's camera property.

    @unittest.skip("Need run manually. And setup camera before.")
    def test_add_camera(self):

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

        from ccmapp.videomgr import videomgr
        videomgr.collect()
        videos = Video.objects.all()
        self.assertEqual(1, len(videos))
        video = videos[0]
        self.assertTrue(video.url_path.find('static/videos/1-762881292') == 0)

    def test_project_ordering(self):
        self._force_authenticate()
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
        self._force_authenticate()
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




    def test_upload_video(self):
        # TODO
        pass

    def test_month_project_report(self):
        # TODO.
        pass


class AuthApiTest(CcmApiTestCase):
    def test_user_register(self):
        user_model = get_user_model()
        req_body = {user_model.USERNAME_FIELD: "13482777788"}
        url = reverse('ccm_user-register')
        resp = self.client.post(url, req_body, format='json')
        self.assertEqual(status.HTTP_201_CREATED, resp.status_code)

    def test_user_login(self):
        # force authenticate to create a user, then use this user to do login test
        self._force_authenticate()
        user_model = get_user_model()
        req_body = {user_model.USERNAME_FIELD: "13493893332", "password": "123456"}
        url = reverse('ccm_user-list')
        resp = self.client.post(url, req_body, format='json')
        # do login test
        self.assertEqual(status.HTTP_201_CREATED, resp.status_code)
        req_body = {user_model.USERNAME_FIELD: "13493893332", "password": "123456"}
        url = reverse('ccm_user-login')
        resp = self.client.post(url, req_body, format='json')
        self.assertEqual(status.HTTP_200_OK, resp.status_code)

    def test_user_login_failed(self):
        user_model = get_user_model()
        req_body = {user_model.USERNAME_FIELD: "13493893332", "password": "123456"}
        url = reverse('ccm_user-login')
        resp = self.client.post(url, req_body, format='json')
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, resp.status_code)

    def test_change_password(self):
        user_model = get_user_model()
        user = user_model(password="123456", is_active=True)
        setattr(user, user_model.USERNAME_FIELD, "13493893332")
        user.save()
        user = user_model.objects.get(id=user.id)
        self.assertEqual("13493893332", getattr(user, user_model.USERNAME_FIELD))
        self.assertEqual("123456", user.password)
        req_body = {user_model.USERNAME_FIELD: "13493893332"}
        url = reverse('ccm_user-password_change')
        resp = self.client.post(url, req_body, format='json')
        self.assertEqual(status.HTTP_200_OK, resp.status_code)
        user = user_model.objects.get(id=user.id)
        self.assertEqual("13493893332", getattr(user, user_model.USERNAME_FIELD))
        self.assertEqual(False, check_password("123456", user.password))

    def test_access_login_code(self):
        user_model = get_user_model()
        req_body = {user_model.USERNAME_FIELD: "13493893332"}
        url = reverse('ccm_user-access_login_code')
        resp = self.client.post(url, req_body, format='json')
        self.assertEqual(status.HTTP_201_CREATED, resp.status_code)
        try:
            user = user_model.objects.get(**req_body)
        except user_model.DoesNotExist:
            self.fail("test_access_login_code failed.")
        self.assertEqual("13493893332", getattr(user, user_model.USERNAME_FIELD))
        self.assertIsNotNone(user.password)


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
