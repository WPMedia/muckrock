# Generated by Django 2.2.15 on 2020-08-28 20:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foia', '0074_foiafile_dc_legacy'),
    ]

    operations = [
        migrations.AlterField(
            model_name='foiafile',
            name='dc_legacy',
            field=models.BooleanField(default=False),
        ),
    ]
