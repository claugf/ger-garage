from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import *
from .decorators import allowed_users
from .forms import *


@login_required(login_url='pages:login')
@allowed_users(allowed_roles=['customer'])
def index(request):
    return render(request, 'bookings/index.html')


@login_required(login_url='pages:login')
@allowed_users(allowed_roles=['customer'])
def booking(request):
    return render(request, 'bookings/booking.html')


@login_required(login_url='pages:login')
@allowed_users(allowed_roles=['customer'])
def vehicle(request, pk):
    # Pass the customer id pk
    customer = Customer.objects.get(user_id=pk)
    form = VehicleForm(initial={'customer': customer})

    if request.method == "POST":
        print('POSTTT', request.POST)
        form = VehicleForm(request.POST)
        if form.is_valid():
            form.save()

    context = {'form': form}
    return render(request, 'bookings/vehicle.html', context)


@login_required(login_url='pages:login')
@allowed_users(allowed_roles=['admin'])
def dashboard(request):
    return render(request, 'bookings/dashboard.html')
