# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import viewsets

# Create your views here.
from pocket_monitor.db import models, serializers


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = models.Project.objects.all()
    serializer_class = serializers.ProjectSerializer
