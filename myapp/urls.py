from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('track-price/', views.track_price, name='track_price'),
]
