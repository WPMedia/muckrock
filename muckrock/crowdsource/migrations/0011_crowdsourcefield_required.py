# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-01-25 16:46


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crowdsource', '0010_auto_20180125_1615'),
    ]

    operations = [
        migrations.AddField(
            model_name='crowdsourcefield',
            name='required',
            field=models.BooleanField(default=True),
        ),
    ]
