# Generated by Django 4.0 on 2023-06-08 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0006_alter_teammodel_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rolemodel',
            name='role',
            field=models.CharField(max_length=20, unique=True),
        ),
    ]
