# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-29 15:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='failed_logins',
            field=models.SmallIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='profile',
            name='photo',
            field=models.ImageField(blank=True, upload_to=b''),
        ),
    ]
