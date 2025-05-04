# ml/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('predict/', views.prediction_form, name='prediction_form'),
    path('history/', views.history, name='history'),
]