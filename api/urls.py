from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.welcome, name="Swagger"),
    path('register', views.RegisterView.as_view(), name="Registration"),
    path('login', views.LoginView.as_view(), name="Login"),

    path('users/get', views.GetUser.as_view(), name="GetUser"),
    
    path('cards/get', views.GetCardByID.as_view(), name="Get Card By ID"),
    path('cards/create', views.CreateCard.as_view(), name="Create Card"),
    path('cards/user', views.GetUserCards.as_view(), name="Get user cards"),

    path('hotspot/connect', views.ConnectToHotspot.as_view(), name="Connect to hotspot"),
    path('hotspot/cards', views.GetCardsInHotspot.as_view(), name="Get people in hotspot")

]