from __future__ import unicode_literals
from django.db import models
from api_rackian.models import TimeStampedModel
from storage.models import File, Folder


class Permission(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=500)


class FileLink(TimeStampedModel):
    id = models.CharField(primary_key=True, max_length=25)
    file = models.ForeignKey(File, on_delete=models.CASCADE)
    permission = models.ForeignKey(Permission)
    link = models.CharField(max_length=500)


class FolderLink(TimeStampedModel):
    id = models.CharField(primary_key=True, max_length=25)
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE)
    permission = models.ForeignKey(Permission)
    link = models.CharField(max_length=500)
