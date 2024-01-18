from django.urls import path

from . import views

urlpatterns = [
    path('authorization', views.authorization, name='authorization'),
    path('registration', views.registration, name='registration'),
    path('profile', views.profile, name='profile'),
    path('logout', views.logout, name='logout'),
    path('cart', views.cart, name='cart'),
]
