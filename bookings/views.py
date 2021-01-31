from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages

from .models import *
from .decorators import allowed_users
from .forms import *


from django.db import connection


def q_bookings_customer(customer):
    with connection.cursor() as cursor:
        # Raw query to the database to get the last status of the bookings per customer
        cursor.execute('SELECT B.date, B.plate_id, BT.name , BS.status ' +
                       'FROM bookings_booking B ' +
                       'INNER JOIN bookings_vehicle V ON V.plate = B.plate_id ' +
                       'INNER JOIN pages_customer C ON C.id = V.customer_id ' +
                       'INNER JOIN bookings_bookingtype BT ON BT.id = B.booking_type_id ' +
                       'INNER JOIN ( ' +
                       "SELECT BS1.booking_id, BS1.date, (CASE WHEN BS1.status = 'B' THEN 'BOOKED' ELSE 'IN SERVICE' END) AS status " +
                       "FROM bookings_bookingstatus BS1 " +
                       "INNER JOIN ( " +
                       "SELECT BS.booking_id, MAX(BS.date)date " +
                       "FROM bookings_bookingstatus BS " +
                       "WHERE BS.status IN ('B', 'S') " +
                       "GROUP BY BS.booking_id "
                       ") BS2 ON (BS1.booking_id=BS2.booking_id AND BS1.date = BS2.date) " +
                       ") BS ON BS.booking_id = B.id " +
                       'WHERE V.customer_id = %s', [customer])
        q = cursor.fetchall()

    return q


@login_required(login_url='pages:login')
@allowed_users(allowed_roles=['customer'])
def index(request):
    # Getting customer
    customer = Customer.objects.get(user_id=request.user)

    # Getting bookings by customer with status as Booked or In Service
    q = q_bookings_customer(customer.id)

    context = {'bookings': q}

    return render(request, 'bookings/index.html', context)


@ login_required(login_url='pages:login')
@ allowed_users(allowed_roles=['customer'])
def lastbookings(request):
    return render(request, 'bookings/lastbookings.html')


@login_required(login_url='pages:login')
@allowed_users(allowed_roles=['customer'])
def booking(request):

    customer = Customer.objects.get(user_id=request.user)
    plates = Vehicle.objects.filter(customer_id=customer)

    form = BookingForm()

    # Check if there is any vehicle registered for the customer
    # If not, it redirects the user to the Vehicle Form
    if not plates:
        messages.info(request, 'You need to register your vehicle first!')
        return redirect('bookings:vehicle')
    else:
        # If there is any vehicle registered previously, it proceeds with the booking process
        if request.method == "POST":
            form = BookingForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Booking registered successfully!')
                return redirect('bookings:index')

    context = {'form': form, 'plates': plates}
    return render(request, 'bookings/booking.html', context)


@ login_required(login_url='pages:login')
@ allowed_users(allowed_roles=['customer'])
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


@ login_required(login_url='pages:login')
@ allowed_users(allowed_roles=['admin'])
def dashboard(request):
    return render(request, 'bookings/dashboard.html')
