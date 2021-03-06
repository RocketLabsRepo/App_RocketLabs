# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-22 20:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bundles_app', '0003_auto_20170918_2046'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='service',
            name='bundles',
        ),
        migrations.AddField(
            model_name='bundle',
            name='services',
            field=models.ManyToManyField(to='bundles_app.Service'),
        ),
        migrations.AlterField(
            model_name='bundle',
            name='bundle_extra_fee',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True),
        ),
        migrations.AlterField(
            model_name='bundle',
            name='bundle_total_fee',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True),
        ),
    ]
