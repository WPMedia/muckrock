# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2017-01-19 22:27


from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('foia', '0019_auto_20160330_2039'),
    ]

    operations = [
        migrations.CreateModel(
            name='CommunicationError',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('recipient', models.CharField(max_length=255)),
                ('code', models.CharField(max_length=10)),
                ('error', models.TextField(blank=True)),
                ('event', models.CharField(max_length=10)),
                ('reason', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='CommunicationOpen',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('recipient', models.EmailField(max_length=254)),
                ('city', models.CharField(max_length=50)),
                ('region', models.CharField(max_length=10)),
                ('country', models.CharField(max_length=10)),
                ('client_type', models.CharField(max_length=15)),
                ('client_name', models.CharField(max_length=15)),
                ('client_os', models.CharField(max_length=10)),
                ('device_type', models.CharField(max_length=10)),
                ('user_agent', models.CharField(max_length=255)),
                ('ip', models.CharField(max_length=15)),
            ],
        ),
        migrations.AddField(
            model_name='foiacommunication',
            name='confirmed',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='foiacommunication',
            name='opened',
            field=models.BooleanField(default=False, help_text=b'DEPRECATED: If emailed, did we receive an open notification? If faxed, did we recieve a confirmation?'),
        ),
        migrations.AddField(
            model_name='communicationopen',
            name='communication',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='opens', to='foia.FOIACommunication'),
        ),
        migrations.AddField(
            model_name='communicationerror',
            name='communication',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='errors', to='foia.FOIACommunication'),
        ),
    ]
