from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, EmailValidator
from django.conf import settings

from authentication.models import TeamModel


class ClientModel(models.Model):
    first_name = models.CharField(
        max_length=25,
        null=False
        )
    last_name = models.CharField(
        max_length=25,
        null=False,
        )
    email = models.CharField(
        max_length=100,
        validators=[EmailValidator],
        unique=True,
        null=False
    )
    phone = models.IntegerField(
        null=False,
        validators=[MinValueValidator(0), MaxValueValidator(9999999999)]
        )
    mobile = models.IntegerField(
        null=False,
        validators=[MinValueValidator(0), MaxValueValidator(9999999999)]
        )
    compagny_name = models.CharField(
        max_length=250,
        null=False,
        unique=True
        )
    sales_contact = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT
        )
    date_created = models.DateTimeField(
        auto_now_add=True)
    date_updated = models.DateTimeField(
        auto_now=True
        )
    is_prospect = models.BooleanField(
        default=True
        )


class ContractModel(models.Model):
    payment_due = models.DateField(
        null=False,
        )
    date_created = models.DateTimeField(
        auto_now_add=True
        )
    date_updated = models.DateTimeField(
        auto_now=True
        )
    amount = models.DecimalField(
        blank=True,
        null=True,
        max_digits=1000,
        decimal_places=2
        )
    id_client = models.ForeignKey(
        ClientModel,
        on_delete=models.CASCADE
        )


class StatusModel(models.Model):
    status = models.CharField(
        max_length=20,
        null=False,
        unique=True
    )


class EventModel(models.Model):
    event_date = models.DateField(
        null=False
        )
    attenteeds = models.IntegerField(
        null=False
        )
    note = models.CharField(
        null=True,
        blank=True,
        max_length=400
        )
    date_created = models.DateTimeField(
        auto_now_add=True
        )
    date_updated = models.DateTimeField(
        auto_now=True
        )
    status = models.ForeignKey(
        StatusModel,
        on_delete=models.PROTECT
    )
    support_contact = models.ForeignKey(
        TeamModel,
        on_delete=models.PROTECT
    )
    id_contract = models.ForeignKey(
        ContractModel,
        on_delete=models.CASCADE,
        null=False
    )
