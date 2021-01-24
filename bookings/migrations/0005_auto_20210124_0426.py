# Generated by Django 3.1.5 on 2021-01-24 04:26

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0004_auto_20210124_0410'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking_products',
            name='cant',
            field=models.PositiveSmallIntegerField(default=1, validators=[django.core.validators.MaxValueValidator(99)]),
        ),
        migrations.AddField(
            model_name='booking_services',
            name='cant',
            field=models.PositiveSmallIntegerField(default=1, validators=[django.core.validators.MaxValueValidator(99)]),
        ),
    ]
