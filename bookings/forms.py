from django.db.models import fields
from django.forms import ModelForm
from .models import Booking, Vehicle


class VehicleForm(ModelForm):
    class Meta:
        model = Vehicle
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(VehicleForm, self).__init__(*args, **kwargs)
        self.fields['transmission'].required = False


class BookingForm(ModelForm):
    class Meta:
        model = Booking
        fields = ['plate', 'booking_type', 'date', 'comments', ]

    def __init__(self, *args, **kwargs):
        super(BookingForm, self).__init__(*args, **kwargs)
        self.fields['comments'].required = False
