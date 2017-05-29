from __future__ import unicode_literals
import random
import string
from django.contrib.auth.models import AbstractUser
from django.db import models


def custom_identifier():
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(12))


class User(AbstractUser):
    id = models.CharField(primary_key=True, max_length=12, default=custom_identifier)
    space = models.BigIntegerField(default=0)
