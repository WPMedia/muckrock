# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-09-25 13:57


from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('agency', '0024_auto_20190709_1504'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='agency',
            name='payable_to',
        ),
    ]
