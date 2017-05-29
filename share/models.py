from __future__ import unicode_literals
from django.db import models
from api_rackian.models import TimeStampedModel
from storage.models import File, Folder


class Permission(TimeStampedModel):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=500)


class FileLink(TimeStampedModel):
    file = models.ForeignKey(File, on_delete=models.CASCADE)
    shared_permission = models.ForeignKey(Permission)
    link = models.CharField(max_length=500)


class FolderLink(TimeStampedModel):
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE)
    shared_permission = models.ForeignKey(Permission)
    link = models.CharField(max_length=500)
