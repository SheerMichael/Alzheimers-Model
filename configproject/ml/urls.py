from django.urls import path
from . import views

app_name = 'ml'

urlpatterns = [
    path('', views.PredictionFormView.as_view(), name='prediction_form'),
    path('result/', views.PredictionResultView.as_view(), name='prediction_result'),
]