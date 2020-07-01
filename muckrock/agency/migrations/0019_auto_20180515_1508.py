# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-05-15 19:08


from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('agency', '0018_agency_exempt_note'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='agency',
            options={'permissions': (('view_emails', 'Can view private contact information'),), 'verbose_name_plural': 'agencies'},
        ),
        migrations.RemoveField(
            model_name='agency',
            name='manual_stale',
        ),
        migrations.RemoveField(
            model_name='agency',
            name='stale',
        ),
    ]
