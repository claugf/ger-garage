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


def q_bookings_admin():
    with connection.cursor() as cursor:
        # Raw query to the database to get the following bookings
        cursor.execute('SELECT B.id, B.date, B.plate_id, M."name", BT.name , BS.status  ' +
                       'FROM bookings_booking B ' +
                       'INNER JOIN bookings_vehicle V ON V.plate = B.plate_id ' +
                       'INNER JOIN bookings_vehiclemodel M ON M.id = V."vehicleModel_id" ' +
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
                       'WHERE B.date >= NOW() ' +
                       'ORDER BY B.date')
        q = cursor.fetchall()

    return q


@ login_required(login_url='pages:login')
@ allowed_users(allowed_roles=['customer'])
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


@ login_required(login_url='pages:login')
@ allowed_users(allowed_roles=['customer'])
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
                # Obtaining selected date
                dt = form.cleaned_data['date']
                # Query to count how many bookings per day
                bookingsDay = Booking.objects.filter(date__date=dt).count()
                # Limit of bookings per day, it must be 15, set 3 for demo
                limit = 3

                # If bookings HAVE NOT reached the limit, then save the booking
                if bookingsDay < limit:
                    form.save()
                    messages.success(
                        request, 'Booking registered successfully!')
                    return redirect('bookings:index')
                else:
                    # If bookings HAVE reached the limit, then warn the user
                    print("No valid")
                    messages.warning(
                        request, "The limit number of bookings has been reached for this date. Please select other date!")

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
    # Getting following bookings with status as Booked or In Service
    q = q_bookings_admin()

    context = {'bookings': q}
    return render(request, 'bookings/dashboard.html', context)


def update_status_I(request, pk):
    booking = Booking.objects.get(id=pk)
    # Adding a new status as "In-service"
    BookingStatus.objects.create(
        status='S',
        booking=booking,
    )

    # Getting following bookings with status as Booked or In Service
    q = q_bookings_admin()

    context = {'bookings': q}
    return render(request, 'bookings/dashboard.html', context)
