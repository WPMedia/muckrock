# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-30 20:39


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0013_failedfaxtask_reason'),
    ]

    operations = [
        migrations.AlterField(
            model_name='snailmailtask',
            name='category',
            field=models.CharField(choices=[(b'a', b'Appeal'), (b'n', b'New'), (b'u', b'Update'), (b'f', b'Followup')], max_length=1),
        ),
    ]
