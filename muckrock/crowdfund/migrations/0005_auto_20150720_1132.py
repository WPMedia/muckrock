# -*- coding: utf-8 -*-

# Django
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crowdfund', '0004_auto_20150708_2057'),
    ]

    operations = [
        migrations.AlterField(
            model_name='crowdfundrequest',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='crowdfundrequest',
            name='payment_received',
            field=models.DecimalField(
                default='0.00', max_digits=14, decimal_places=2
            ),
        ),
        migrations.AlterField(
            model_name='crowdfundrequest',
            name='payment_required',
            field=models.DecimalField(
                default='0.00', max_digits=14, decimal_places=2
            ),
        ),
        migrations.AlterField(
            model_name='crowdfundrequestpayment',
            name='amount',
            field=models.DecimalField(max_digits=14, decimal_places=2),
        ),
    ]
