# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-03 05:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core_app', '0010_auto_20170911_1145'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='photo',
            field=models.ImageField(blank=True, default='../media/photo_profile/default_user_3x2.png', upload_to='photo_profile'),
        ),
    ]