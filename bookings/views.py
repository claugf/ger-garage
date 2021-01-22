from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import *
from .decorators import allowed_users


@login_required(login_url='pages:login')
@allowed_users(allowed_roles=['customer'])
def index(request):
    return render(request, 'bookings/index.html')


@login_required(login_url='pages:login')
@allowed_users(allowed_roles=['customer'])
def booking(request):
    return render(request, 'bookings/booking.html')


@login_required(login_url='pages:login')
@allowed_users(allowed_roles=['admin'])
def dashboard(request):
    return render(request, 'bookings/dashboard.html')
