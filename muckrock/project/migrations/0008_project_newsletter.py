# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-12 17:28

# Django
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0007_auto_20160303_1229'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='newsletter',
            field=models.CharField(
                blank=True, help_text='The MailChimp list id.', max_length=255
            ),
        ),
    ]
