# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-30 17:20


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foia', '0039_auto_20171017_1023'),
    ]

    operations = [
        migrations.AddField(
            model_name='foiacommunication',
            name='hidden',
            field=models.BooleanField(default=False),
        ),
    ]
