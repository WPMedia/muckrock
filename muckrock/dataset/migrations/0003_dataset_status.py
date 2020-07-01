# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-12-11 14:53


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dataset', '0002_auto_20171211_1106'),
    ]

    operations = [
        migrations.AddField(
            model_name='dataset',
            name='status',
            field=models.CharField(choices=[(b'processing', b'Processing'), (b'error', b'Error'), (b'ready', b'Ready')], default=b'ready', max_length=10),
        ),
    ]
