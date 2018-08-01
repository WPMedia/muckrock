# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-08-07 13:25
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('crowdsource', '0018_auto_20180627_1124'),
    ]

    operations = [
        migrations.AddField(
            model_name='crowdsourceresponse',
            name='edit_datetime',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='crowdsourceresponse',
            name='edit_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='edited_crowdsource_responses', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='crowdsourcevalue',
            name='original_value',
            field=models.CharField(blank=True, max_length=2000),
        ),
        migrations.AlterField(
            model_name='crowdsourcevalue',
            name='value',
            field=models.CharField(blank=True, max_length=2000),
        ),
    ]
