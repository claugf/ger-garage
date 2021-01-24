# Generated by Django 3.1.5 on 2021-01-24 03:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0003_nonworkingday'),
        ('bookings', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('comments', models.CharField(max_length=500, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='BookingType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('cost', models.DecimalField(decimal_places=2, max_digits=7)),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('cost', models.DecimalField(decimal_places=2, max_digits=7)),
            ],
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='engine_type',
            field=models.CharField(choices=[('MANUAL', 'MANUAL'), ('AUTOMATIC', 'AUTOMATIC'), ('HYBRID', 'HYBRID'), ('ELECTRIC', 'ELECTRIC')], max_length=10, null=True),
        ),
        migrations.CreateModel(
            name='BookingStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('B', 'Booked'), ('S', 'In Service'), ('F', 'Fixed/Completed'), ('C', 'Collected'), ('S', 'Unrepairable')], default='B', max_length=1)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('booking', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bookings.booking')),
            ],
        ),
        migrations.AddField(
            model_name='booking',
            name='booking_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bookings.bookingtype'),
        ),
        migrations.AddField(
            model_name='booking',
            name='plate',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bookings.vehicle'),
        ),
        migrations.AddField(
            model_name='booking',
            name='products',
            field=models.ManyToManyField(to='bookings.Product'),
        ),
        migrations.AddField(
            model_name='booking',
            name='services',
            field=models.ManyToManyField(to='bookings.Service'),
        ),
        migrations.AddField(
            model_name='booking',
            name='staff',
            field=models.ManyToManyField(to='pages.Staff'),
        ),
    ]
