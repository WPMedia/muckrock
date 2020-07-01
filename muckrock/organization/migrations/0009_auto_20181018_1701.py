# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-10-18 21:01


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0008_auto_20181017_1645'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='individual',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='organization',
            name='org_type',
            field=models.IntegerField(default=2),
            preserve_default=False,
        ),
    ]
