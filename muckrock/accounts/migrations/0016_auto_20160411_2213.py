# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-11 22:13
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('agency', '0008_agency_requires_proxy'),
        ('accounts', '0015_auto_20160208_1923'),
    ]

    operations = [
        migrations.CreateModel(
            name='AgencyProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('agency', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='members', to='agency.Agency')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterField(
            model_name='profile',
            name='acct_type',
            field=models.CharField(choices=[(b'admin', b'Admin'), (b'basic', b'Basic'), (b'beta', b'Beta'), (b'pro', b'Professional'), (b'proxy', b'Proxy'), (b'robot', b'Robot'), (b'agency', b'Agency')], max_length=10),
        ),
    ]
