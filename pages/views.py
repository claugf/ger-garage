from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

from django.contrib import messages
from django.core import exceptions
from django.http.response import HttpResponseForbidden

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

from .forms import CreateUserForm
from .decorators import authenticated_user, allowed_users


# @authenticated_user
def index(request):
    # GERSGARAGE INDEX
    return render(request, 'pages/index.html')


@authenticated_user
def register(request):
    #   REGISTER USER
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            group = Group.objects.get(name="customer")
            user.groups.add(group)

            messages.success(
                request, 'You have been registered sucessfully, please Log In!')
            return redirect('pages:login')

    context = {'form': form}
    return render(request, 'pages/register.html', context)


@authenticated_user
def loginPage(request):
    # LOGGING USER
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            group = user.groups.all()[0].name
            print(group)
            if group == "admin":
                return redirect('bookings:dashboard')
            else:
                return redirect('bookings:index')
        else:
            messages.info(request, 'Username OR Password is incorrect')

    context = {}
    return render(request, 'pages/login.html', context)


def logoutUser(request):
    # LOGOUT USER
    logout(request)
    messages.info(request, 'You are logged out!')
    return redirect('pages:login')


def unauthorizedpage(request, exception):
    # PAGE 403 CODE
    return render(request, 'pages/403_csrf.html')


def notfoundpage(request, exception):
    # PAGE 404 CODE
    return render(request, 'pages/404code.html')


def errorpage(request):
    # PAGE 500 CODE
    return render(request, 'pages/500code.html')


def errordemopage(request):
    # PAGE TO TEST 500 CODE
    return render('pages:doesnotexist')


def services(request):
    # GERSGARAGE SERVICES PAGE
    return render(request, 'pages/services.html')


def about(request):
    # GERSGARAGE ABOUT US
    return render(request, 'pages/about.html')


@login_required(login_url='pages:login')
@allowed_users(allowed_roles=['customer'])
def customer_settings(request):
    # CUSTOMER PROFILE
    return render(request, 'pages/settings.html')
