# from gersgarage.pages.models import Customer, Staff
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.validators import RegexValidator
from django.utils.translation import gettext as _

import datetime

from pages.models import Customer, Staff


class Make(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)

    def __str__(self):
        return self.name


class VehicleType(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)

    def __str__(self):
        return self.name


class VehicleModel(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)
    make = models.ForeignKey(Make, on_delete=models.CASCADE)
    vehicleType = models.ForeignKey(VehicleType, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


def current_year():
    # Function to get current year
    return datetime.date.today().year


def max_value_current_year(value):
    # Function to validate the current year as maximun value
    return MaxValueValidator(current_year())(value)


class Vehicle(models.Model):
    COLOR = (
        ('Black', 'Black'),
        ('White', 'White'),
        ('Red', 'Red'),
        ('Blue', 'Blue'),
        ('Brown', 'Brown'),
        ('Other', 'Other'),
    )
    ENGINE_TYPE = (
        ('MANUAL', 'MANUAL'),
        ('AUTOMATIC', 'AUTOMATIC'),
        ('HYBRID', 'HYBRID'),
        ('ELECTRIC', 'ELECTRIC'),
    )
    FUEL = (
        ('PETROL', 'PETROL'),
        ('DIESEL', 'DIESEL'),
        ('GAS', 'GAS'),
    )
    plate = models.CharField(max_length=11, primary_key=True, validators=[
                             RegexValidator('^[A-Z0-9]+(-[A-Z0-9]+)*$', 'Only numbers, uppercase letters and dashes allowed.')])
    color = models.CharField(max_length=10, choices=COLOR, null=True)
    year = models.PositiveSmallIntegerField(
        _('year'), validators=[MinValueValidator(1920), max_value_current_year], null=True)
    engine_type = models.CharField(
        max_length=10, choices=ENGINE_TYPE, null=True)
    transmission = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(800), MaxValueValidator(10000)], null=True)
    fuel = models.CharField(max_length=10, choices=FUEL, null=True)
    vehicleModel = models.ForeignKey(
        VehicleModel, on_delete=models.CASCADE, null=False)
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, null=False)

    def __str__(self):
        return self.plate


class Product(models.Model):
    name = models.CharField(max_length=150, null=False, blank=False)
    cost = models.DecimalField(max_digits=7, decimal_places=2, null=False)

    def __str__(self):
        return self.name


class Service(models.Model):
    name = models.CharField(max_length=150, null=False, blank=False)
    cost = models.DecimalField(max_digits=7, decimal_places=2, null=False)

    def __str__(self):
        return self.name


class BookingType(models.Model):
    name = models.CharField(max_length=150, null=False, blank=False)
    cost = models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(9999)], null=False)

    def __str__(self):
        return self.name


class Booking(models.Model):
    date = models.DateTimeField(null=False)
    comments = models.CharField(max_length=500, null=True)
    booking_type = models.ForeignKey(
        BookingType, on_delete=models.CASCADE, null=False)
    plate = models.ForeignKey(Vehicle, on_delete=models.CASCADE, null=False)
    staff = models.ManyToManyField(Staff)
    products = models.ManyToManyField(Product, through='Booking_Products')
    services = models.ManyToManyField(Service, through='Booking_Services')

    def __str__(self):
        return self.date


class Booking_Products(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, null=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=False)
    cant = models.PositiveSmallIntegerField(
        default=1, validators=[MaxValueValidator(99)], null=False)


class Booking_Services(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, null=False)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, null=False)
    cant = models.PositiveSmallIntegerField(
        default=1, validators=[MaxValueValidator(99)], null=False)


class BookingStatus(models.Model):
    STATUS = (
        ('B', 'Booked'),
        ('S', 'In Service'),
        ('F', 'Fixed/Completed'),
        ('C', 'Collected'),
        ('S', 'Unrepairable'),
    )
    status = models.CharField(
        max_length=1, choices=STATUS, default='B', null=False)
    date = models.DateTimeField(auto_now_add=True, null=False)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, null=False)

    def __str__(self):
        return self.status
