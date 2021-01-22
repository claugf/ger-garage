from django.urls import path

from . import views

app_name = 'pages'

urlpatterns = [
    path('', views.index, name="index"),
    path('register/', views.register, name="register"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('403code/', views.unauthorizedpage, name="403code"),

    path('services/', views.services, name="services"),
    path('about/', views.about, name="about"),
    path('settings/', views.customer_settings, name="settings")
]
