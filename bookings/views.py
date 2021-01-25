from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages

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
    messages.success(request, 'PEPEEEE')
    return render(request, 'bookings/booking.html')


@login_required(login_url='pages:login')
@allowed_users(allowed_roles=['customer'])
def vehicle(request):
    # Get customer from logged user
    customer = Customer.objects.get(user_id=request.user)

    form = VehicleForm(initial={'customer': customer})

    makes = Make.objects.all()
    vmodels = VehicleModel.objects.all()
    if request.method == "POST":
        form = VehicleForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Vehicle registered successfully!')
            return redirect('bookings:booking')

    context = {'form': form, 'makes': makes,
               'vmodels': vmodels, 'customer': customer}
    return render(request, 'bookings/vehicle.html', context)


def get_json_model_data(request, *args, **kwargs):
    # Getting all models from a selected make
    selected_make = kwargs.get('pk')
    obj_models = list(VehicleModel.objects.filter(
        make_id=selected_make).values())
    return JsonResponse({'data': obj_models})


@login_required(login_url='pages:login')
@allowed_users(allowed_roles=['admin'])
def dashboard(request):
    return render(request, 'bookings/dashboard.html')
