# Generated by Django 2.2.15 on 2020-09-11 13:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('foia', '0076_auto_20200911_0943'),
    ]

    operations = [
        migrations.RenameField(
            model_name='foiafile',
            old_name='access',
            new_name='old_access',
        ),
    ]
