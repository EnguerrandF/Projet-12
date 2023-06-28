from django.contrib.auth.models import AbstractUser
from django.db import models


class RoleModel(models.Model):
    role = models.CharField(
        max_length=20,
        null=False,
        blank=False,
        unique=True)


class TeamModel(AbstractUser):
    role = models.ForeignKey(RoleModel, on_delete=models.PROTECT, null=False, blank=False)

    REQUIRED_FIELDS = ["first_name", "last_name"]
