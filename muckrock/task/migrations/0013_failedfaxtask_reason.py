# -*- coding: utf-8 -*-

# Django
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0012_auto_20160228_1100'),
    ]

    operations = [
        migrations.AddField(
            model_name='failedfaxtask',
            name='reason',
            field=models.CharField(default='', max_length=255, blank=True),
        ),
    ]
