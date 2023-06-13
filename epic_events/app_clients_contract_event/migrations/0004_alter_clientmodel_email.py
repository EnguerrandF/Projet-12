# Generated by Django 4.0 on 2023-06-12 07:56

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_clients_contract_event', '0003_alter_clientmodel_compagny_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientmodel',
            name='email',
            field=models.CharField(max_length=100, unique=True, validators=[django.core.validators.EmailValidator, django.core.validators.MinLengthValidator(3)]),
        ),
    ]
