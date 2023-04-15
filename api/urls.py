from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.welcome, name="Swagger"),
    path('register', views.RegisterView.as_view(), name="Registration"),
    path('login', views.LoginView.as_view(), name="Login"),

    path('users/get', views.GetUser.as_view(), name="GetUser"),
    
    path("cards/get", views.GetCardByID.as_view(), name="Get card by id"),
    path("cards/create", views.CreateCard.as_view(), name="Create Card"),
    #path("cards/send_wifi", views.SendWifiHotspot.as_view(), name="Send Wifi Hotspot"),

]