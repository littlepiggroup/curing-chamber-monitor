# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.


# Company and projects
class Company(models.Model):
    name = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)


class Project(models.Model):
    name = models.CharField(max_length=20)
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')
    code = models.TextField()
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    class Meta:
        ordering = ('-created', 'code')


# Sample website credential, sample, sample alert
class SampleWebSiteCredential(models.Model):
    user = models.CharField(max_length=10)
    password = models.CharField(max_length=10)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)


class Sample(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    #TODO: enum -- shui ni, hun ning tu, ...
    sample_type = models.CharField(max_length=20)
    yanghu_tiaojian = models.CharField(max_length=50)
    result = models.CharField(max_length=50)
    # >= 0  %
    percentage = models.IntegerField()


class SampleAlert(models.Model):
    sample = models.ForeignKey(Sample)
    # Created, fixing, closed.
    status = models.CharField(max_length=10)
    create_time = models.DateTimeField()
    created_by = models.CharField(max_length=10)
    update_time = models.DateTimeField()
    updated_by = models.CharField(max_length=10)


# Camera, video and video_alert
class Camera(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    device_number = models.CharField(max_length=50)


class Video(models.Model):
    camera = models.ForeignKey(Camera, on_delete=models.CASCADE)
    #In seconds
    duration = models.IntegerField()
    # relative url
    url = models.CharField(max_length=50)


# video alert may be created by user.
class VideoAlert(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    # auto, manual
    alert_type = models.CharField(max_length=10)
    status = models.CharField(max_length=10)
    create_time = models.DateTimeField()
    created_by = models.CharField(max_length=10)
    update_time = models.DateTimeField()
    updated_by = models.CharField(max_length=10)


# Sensor, temperature_humidity data, sensor_alert
class Sensor(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    device_number = models.CharField(max_length=50)
    #TODO: enum -- temperature, humidity.
    sensor_type = models.CharField(max_length=20)

class TempHumdtyData(models.Model):
    pass


class TempHumdtyAlert(models.Model):
    status = models.CharField(max_length=10)
    create_time = models.DateTimeField()
    created_by = models.CharField(max_length=10)
    update_time = models.DateTimeField()
    updated_by = models.CharField(max_length=10)


# TODO: Alert notification and subscribe.




