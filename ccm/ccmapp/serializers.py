# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers
from ccm.ccmapp import models


class BuildingCompanySerializer(serializers.ModelSerializer):
    users = serializers.PrimaryKeyRelatedField(many=True,
                                               queryset=models.BuildingCompanyUser.objects.all(),
                                               required=False)
    projects = serializers.PrimaryKeyRelatedField(many=True, queryset=models.Project.objects.all(), required=False)

    class Meta:
        model = models.BuildingCompany
        fields = '__all__'
        depth = 1


class BuildingCompanyUserSerializer(serializers.ModelSerializer):
    building_company = serializers.PrimaryKeyRelatedField(many=False,
                                                          queryset=models.BuildingCompany.objects.all(), required=False)

    class Meta:
        model = models.BuildingCompanyUser
        fields = '__all__'
        depth = 1


class ProjectNameSerializer(serializers.ModelSerializer):
    project = serializers.PrimaryKeyRelatedField(many=False, queryset=models.Project.objects.all(), required=False)

    class Meta:
        model = models.ProjectName
        fields = '__all__'
        depth = 1


class ProjectSerializer(serializers.ModelSerializer):
    contracts = serializers.PrimaryKeyRelatedField(many=True, queryset=models.Contract.objects.all(), required=False)
    building_company = serializers.PrimaryKeyRelatedField(many=False,
                                                          queryset=models.BuildingCompany.objects.all())
    names = ProjectNameSerializer(many=True, read_only=False)

    class Meta:
        model = models.Project
        fields = '__all__'
        depth = 1

    def create(self, validated_data):
        names_data = validated_data.pop('names')
        project = models.Project.objects.create(**validated_data)

        for name_data in names_data:
            models.ProjectName.objects.create(project=project, **name_data)
        return project


class ContractSerializer(serializers.ModelSerializer):
    project = serializers.PrimaryKeyRelatedField(many=False, queryset=models.Project.objects.all())

    class Meta:
        model = models.Contract
        fields = '__all__'
        depth = 1


class SampleSerializer(serializers.ModelSerializer):
    contract = serializers.PrimaryKeyRelatedField(many=False, queryset=models.Contract.objects.all())

    class Meta:
        model = models.Sample
        fields = '__all__'
        depth = 1
