from django.http import HttpResponse
from django.http.response import HttpResponseForbidden
from django.shortcuts import redirect
from django.core import exceptions


def authenticated_user(view_func):
    # Stop users to see the login and register page, once they are authenticated
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            group = request.user.groups.all()[0].name
            if group == "admin":
                return redirect('bookings:dashboard')
            else:
                return redirect('bookings:index')
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func


def allowed_users(allowed_roles=[]):
    # Check if the user if allowed to access the view
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):

            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name

            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                raise exceptions.PermissionDenied

        return wrapper_func

    return decorator
