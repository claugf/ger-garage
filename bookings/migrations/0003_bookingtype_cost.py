# Generated by Django 3.1.5 on 2021-01-24 03:50

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0002_auto_20210124_0337'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookingtype',
            name='cost',
            field=models.PositiveSmallIntegerField(default=1, validators=[django.core.validators.MaxValueValidator(9999)]),
            preserve_default=False,
        ),
    ]
