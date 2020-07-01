# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-11-28 13:18


from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('foia', '0042_foiarequest_portal_password'),
    ]

    operations = [
        migrations.CreateModel(
            name='CommunicationMoveLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField(auto_now_add=True)),
                ('communication', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='foia.FOIACommunication')),
                ('foia', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='foia.FOIARequest')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
