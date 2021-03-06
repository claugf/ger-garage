# Generated by Django 3.1.5 on 2021-01-24 04:10

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0003_bookingtype_cost'),
    ]

    operations = [
        migrations.CreateModel(
            name='Booking_Services',
            fields=[
                ('id', models.AutoField(auto_created=True,
                                        primary_key=True, serialize=False, verbose_name='ID')),
                ('booking', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE, to='bookings.booking')),
                ('service', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE, to='bookings.service')),
            ],
        ),
        migrations.CreateModel(
            name='Booking_Products',
            fields=[
                ('id', models.AutoField(auto_created=True,
                                        primary_key=True, serialize=False, verbose_name='ID')),
                ('booking', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE, to='bookings.booking')),
                ('product', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE, to='bookings.product')),
            ],
        ),
        migrations.AddField(
            model_name='booking',
            name='products',
            field=models.ManyToManyField(
                through='bookings.Booking_Products', to='bookings.Product'),
        ),
        migrations.AddField(
            model_name='booking',
            name='services',
            field=models.ManyToManyField(
                through='bookings.Booking_Services', to='bookings.Service'),
        ),
    ]
