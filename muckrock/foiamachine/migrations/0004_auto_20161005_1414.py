# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2016-10-05 14:14


from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('foiamachine', '0003_foiamachinerequest_sharing_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='foiamachinecommunication',
            name='date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
