# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-30 23:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core_app', '0002_auto_20170829_2058'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='secret_link',
            field=models.CharField(blank=True, max_length=50, unique=True),
        ),
    ]