# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-29 17:02
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import projects_app.models


class Migration(migrations.Migration):

    dependencies = [
        ('projects_app', '0002_auto_20170829_1124'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='bundle',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='bundles_app.Bundle'),
        ),
        migrations.AlterField(
            model_name='project',
            name='current_stage',
            field=models.CharField(blank=True, default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='project',
            name='demo_link',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='project',
            name='description',
            field=models.TextField(blank=True, default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='project',
            name='done_percentage',
            field=models.SmallIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='project',
            name='estimated_duration',
            field=models.CharField(blank=True, default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='project',
            name='owner_comment',
            field=models.TextField(blank=True, default='', max_length=500),
        ),
        migrations.AlterField(
            model_name='project',
            name='str_duration',
            field=models.CharField(blank=True, default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='screenshot',
            name='screenshot',
            field=models.ImageField(upload_to=projects_app.models.screenshot_directory_path),
        ),
    ]