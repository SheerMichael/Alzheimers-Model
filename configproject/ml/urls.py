from django.urls import path
from . import views

urlpatterns = [
    path('', views.PredictionFormView.as_view(), name='input_form'),

  # Fix here
]