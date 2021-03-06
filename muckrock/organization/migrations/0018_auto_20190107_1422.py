# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2019-01-07 19:22


from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0017_membership_admin'),
    ]

    operations = [
        migrations.CreateModel(
            name='Plan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('slug', models.SlugField(max_length=255, unique=True)),
                ('minimum_users', models.PositiveSmallIntegerField(default=1)),
                ('base_requests', models.PositiveSmallIntegerField(default=0)),
                ('requests_per_user', models.PositiveSmallIntegerField(default=0)),
                ('feature_level', models.PositiveSmallIntegerField(default=0)),
            ],
        ),
        migrations.AlterField(
            model_name='organization',
            name='date_update',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='organization',
            name='new_plan',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='organization.Plan'),
        ),
    ]
