from __future__ import unicode_literals

import os

from django.db import models
from authentication.models import User
from api_rackian.models import TimeStampedModel
import random
import string
from api_rackian.settings import STORAGE_FOLDER_ABS


def file_path(instance, filename):
    return "%s/%s" % (STORAGE_FOLDER_ABS, instance.id)


class Folder(TimeStampedModel):
    id = models.CharField(primary_key=True, max_length=25)
    user = models.ForeignKey(User)
    parent_folder = models.ForeignKey('self', null=True)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500, blank=True)

    def delete(self, using=None, keep_parents=False):
        self.user.space = self.user.space - self.folder_space(0)
        if self.user.space < 0:
            self.user.space = 0
        self.delete_files()
        super(Folder, self).delete(using, keep_parents)
        self.user.save()

    def folder_space(self, space):
        files = File.objects.filter(folder=self)
        for current_file in files:
            space += current_file.size
        sub_folders = Folder.objects.filter(parent_folder=self)
        print sub_folders
        if len(sub_folders) > 0:
            for sub_folder in sub_folders:
                return sub_folder.folder_space(space)
        else:
            return space

    def delete_files(self):
        files = File.objects.filter(folder=self)
        for current_file in files:
            file_location = current_file.link.name
            os.remove(file_location)

        sub_folders = Folder.objects.filter(parent_folder=self)
        if len(sub_folders) > 0:
            for sub_folder in sub_folders:
                return sub_folder.delete_files()


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

    def delete(self, using=None, keep_parents=False):
        self.user.space = self.user.space - self.size
        if self.user.space < 0:
            self.user.space = 0
        file_location = self.link.name
        super(File, self).delete(using, keep_parents)
        self.user.save()
        os.remove(file_location)
