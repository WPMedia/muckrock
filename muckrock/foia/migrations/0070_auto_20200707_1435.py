# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2020-07-07 18:35
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('foia', '0069_auto_20190718_1424'),
    ]

    operations = [
        migrations.AlterField(
            model_name='foiarequest',
            name='crowdfund',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='foia', to='crowdfund.Crowdfund'),
        ),
        migrations.AlterField(
            model_name='foiasavedsearch',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
    ]
