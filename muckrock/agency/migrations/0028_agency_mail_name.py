# Generated by Django 2.2.15 on 2020-10-16 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agency', '0027_auto_20200707_1443'),
    ]

    operations = [
        migrations.AddField(
            model_name='agency',
            name='mail_name',
            field=models.CharField(default='', max_length=40),
            preserve_default=False,
        ),
    ]
