# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField

from .models import Project, Company


class CompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = Company
        fields = '__all__'
        depth = 1


class ProjectSerializer(serializers.ModelSerializer):
    company = PrimaryKeyRelatedField(queryset=Company.objects.all())

    class Meta:
        model = Project
        fields = '__all__'
        depth = 1
