from django.db import models
from django.contrib.auth.models import User

# Makes the email a required field
User._meta.get_field('email')._unique = True
User._meta.get_field('email').blank = False
User._meta.get_field('email').null = False


class Customer(models.Model):
    user = models.OneToOneField(
        User, null=False, blank=False, on_delete=models.CASCADE)
    date_of_birth = models.DateTimeField(null=True)
    phone = models.CharField(max_length=10, null=True)
    address = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.user.username


class Title(models.Model):
    name = models.CharField(max_length=100, null=True)
    description = models.CharField(max_length=150, null=True)

    def __str__(self):
        return self.name


class Staff(models.Model):
    user = models.OneToOneField(
        User, null=False, blank=False, on_delete=models.CASCADE)
    date_of_birth = models.DateTimeField(null=True)
    phone = models.CharField(max_length=10, null=True)
    address = models.CharField(max_length=100, null=True)
    hiring_date = models.DateTimeField(auto_now_add=True, null=True)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class NonWorkingDay(models.Model):
    date = models.DateField(primary_key=True)
