# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-03-23 19:48
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('foia', '0054_auto_20180323_1222'),
    ]

    operations = [
        migrations.RenameField(
            model_name='foiarequest',
            old_name='date_done',
            new_name='datetime_done',
        ),
        migrations.RenameField(
            model_name='foiarequest',
            old_name='date_updated',
            new_name='datetime_updated',
        ),
    ]
