# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-08-27 19:50


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foia', '0060_auto_20180713_1455'),
    ]

    operations = [
        migrations.AddField(
            model_name='foiarequest',
            name='deleted',
            field=models.BooleanField(default=False, help_text=b'This request has been "deleted" and should reject new communications'),
        ),
    ]
