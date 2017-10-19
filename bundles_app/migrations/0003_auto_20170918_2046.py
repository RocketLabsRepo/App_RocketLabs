# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-19 00:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bundles_app', '0002_auto_20170918_2044'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service',
            name='service_fee',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=3, null=True),
        ),
        migrations.AlterField(
            model_name='service',
            name='visual_aid',
            field=models.ImageField(blank=True, null=True, upload_to=b''),
        ),
    ]
