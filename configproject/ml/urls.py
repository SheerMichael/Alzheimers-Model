from django.urls import path
from . import views

urlpatterns = [
    path('', views.AlzheimersInputView.as_view(), name='alzheimers_input'),
    path('result/<int:pk>/', views.AlzheimersResultView.as_view(), name='alzheimers_result'),
    path('history/', views.AlzheimersHistoryView.as_view(), name='alzheimers_history'),
    path('api/predict/', views.AlzheimersAPIView.as_view(), name='alzheimers_api'),
]