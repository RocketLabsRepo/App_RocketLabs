# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-03 11:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core_app', '0004_auto_20170830_2003'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='photo',
            field=models.ImageField(blank=True, default='default-user.png', upload_to='photo_profile'),
        ),
    ]