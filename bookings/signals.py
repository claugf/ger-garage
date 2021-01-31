from django.db.models.signals import post_save
from .models import Booking, BookingStatus


def addStatus(sender, instance, created, **kwargs):
    # Insert a booking Status as "Booked" once a booking is registered throught the system
    if created:

        BookingStatus.objects.create(
            status='B',
            booking=instance,
        )
        print('BookingStatus created!')


post_save.connect(addStatus, sender=Booking)
