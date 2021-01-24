from django.db.models.signals import post_save
from django.contrib.auth.models import User, Group
from .models import Customer


def customer_profile(sender, instance, created, **kwargs):
    # Insert a customer register once a user is registered throught the web
    if created:
        group = Group.objects.get(name='customer')
        instance.groups.add(group)

        Customer.objects.create(
            user=instance,
        )
        print('Customer Profile created!')


post_save.connect(customer_profile, sender=User)
