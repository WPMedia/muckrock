# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-10-16 16:02
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0044_auto_20180803_1311'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='organization',
            field=models.ForeignKey(blank=True, db_column=b'organization', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='members', to='organization.Organization'),
        ),
    ]