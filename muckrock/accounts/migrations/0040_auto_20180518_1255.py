# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-05-18 16:55

# Django
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0039_auto_20180418_1122'),
    ]

    operations = [
        migrations.AddField(
            model_name='statistics',
            name='crowdsource_responses_admin',
            field=models.IntegerField(
                blank=True,
                null=True,
                verbose_name='assignment responses admin'
            ),
        ),
        migrations.AddField(
            model_name='statistics',
            name='crowdsource_responses_basic',
            field=models.IntegerField(
                blank=True,
                null=True,
                verbose_name='assignment responses basic'
            ),
        ),
        migrations.AddField(
            model_name='statistics',
            name='crowdsource_responses_beta',
            field=models.IntegerField(
                blank=True, null=True, verbose_name='assignment responses beta'
            ),
        ),
        migrations.AddField(
            model_name='statistics',
            name='crowdsource_responses_pro',
            field=models.IntegerField(
                blank=True, null=True, verbose_name='assignment responses pro'
            ),
        ),
        migrations.AddField(
            model_name='statistics',
            name='crowdsource_responses_proxy',
            field=models.IntegerField(
                blank=True,
                null=True,
                verbose_name='assignment responses proxy'
            ),
        ),
    ]
