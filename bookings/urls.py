from django.urls import path

from . import views

app_name = 'bookings'

urlpatterns = [
    path('', views.index, name="index"),
    path('booking/', views.booking, name="booking"),
    path('vehicle/<str:pk>', views.vehicle, name="vehicle"),
    path('dashboard/', views.dashboard, name="dashboard")
]
