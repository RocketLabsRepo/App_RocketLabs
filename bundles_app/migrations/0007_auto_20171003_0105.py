# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-03 05:05
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bundles_app', '0006_auto_20170923_0853'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bundle',
            options={'ordering': ['id']},
        ),
    ]
