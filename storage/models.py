from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from api_rackian.models import TimeStampedModel


class Folder(TimeStampedModel):
    user = models.ForeignKey(User)
    parent_folder = models.ForeignKey('self', null=True)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500, blank=True)
    path = models.FilePathField(unique=True)


class File(TimeStampedModel):
    user = models.ForeignKey(User)
    folder = models.ForeignKey(Folder)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500, blank=True)
    size = models.BigIntegerField()
    mime_type = models.CharField(max_length=100)
    path = models.FileField()
