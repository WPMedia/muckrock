# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2017-05-25 22:07
from __future__ import unicode_literals

import django.core.files.storage
from django.db import migrations, models
import easy_thumbnails.fields


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0027_auto_20170423_2126'),
    ]

    operations = [
        migrations.AddField(
            model_name='statistics',
            name='total_users_excluding_agencies',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
