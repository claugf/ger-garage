from django.urls import path

from . import views

app_name = 'pages'

urlpatterns = [
    path('', views.index, name="index"),
    path('register/', views.register, name="register"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),

    path('error_page/', views.errordemopage, name="error_page"),

    path('services/', views.services, name="services"),
    path('about/', views.about, name="about"),
    path('settings/', views.customer_settings, name="settings")
]
