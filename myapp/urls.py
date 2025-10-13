from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('track-price/', views.track_price, name='track_price'),
    path('convert-affiliate/', views.convert_affiliate, name='convert_affiliate'),
]
