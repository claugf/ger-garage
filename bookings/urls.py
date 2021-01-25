from django.urls import path

from . import views

app_name = 'bookings'

urlpatterns = [
    path('', views.index, name="index"),
    path('booking/', views.booking, name="booking"),
    path('vehicle/', views.vehicle, name="vehicle"),
    path('vehicle/models-json/<str:pk>/',
         views.get_json_model_data, name="models-json"),
    path('dashboard/', views.dashboard, name="dashboard")
]
