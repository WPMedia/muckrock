# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2017-03-27 21:29

# Django
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agency', '0009_agency_manual_stale'),
        ('accounts', '0025_auto_20170327_1445'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='agency',
            field=models.OneToOneField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to='agency.Agency'
            ),
        ),
        migrations.AlterField(
            model_name='profile',
            name='acct_type',
            field=models.CharField(
                choices=[('admin', 'Admin'), ('basic', 'Basic'),
                         ('beta', 'Beta'), ('pro', 'Professional'),
                         ('proxy', 'Proxy'), ('robot',
                                              'Robot'), ('agency', 'Agency')],
                max_length=10
            ),
        ),
    ]
