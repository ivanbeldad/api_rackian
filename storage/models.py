from __future__ import unicode_literals
from django.db import models
from authentication.models import User
from api_rackian.models import TimeStampedModel
import random
import string
from api_rackian.settings import STORAGE_FOLDER_ABS


# def custom_identifier():
#     return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(12))


def file_path(instance, filename):
    return "%s/%s" % (STORAGE_FOLDER_ABS, instance.id)


class Folder(TimeStampedModel):
    id = models.CharField(primary_key=True, max_length=25)
    user = models.ForeignKey(User)
    parent_folder = models.ForeignKey('self', null=True)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500, blank=True)

    # def save(self, *args, **kwargs):
    #     self.id = self.user.id + '-' + custom_identifier()
    #     super(Folder, self).save(*args, **kwargs)


class File(TimeStampedModel):
    id = models.CharField(primary_key=True, max_length=25)
    user = models.ForeignKey(User)
    folder = models.ForeignKey(Folder, null=True)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500, blank=True)
    size = models.BigIntegerField()
    mime_type = models.CharField(max_length=100, blank=False)
    extension = models.CharField(max_length=20, blank=True)
    link = models.FileField(upload_to=file_path)

    # def save(self, *args, **kwargs):
    #     self.id = self.user.id + '-' + custom_identifier()
    #     super(File, self).save(*args, **kwargs)
