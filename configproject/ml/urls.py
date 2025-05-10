# ml/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # entry point → new assessment form
    path('', views.PredictionFormView.as_view(), name='input_form'),

    # alias if you still want /assessment/ pointing to the same form
    path('assessment/', views.PredictionFormView.as_view(), name='prediction_form'),

    # dashboard: overall stats + recent
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),

    # history list & CRUD
    path('history/', views.AssessmentListView.as_view(), name='assessment_history'),
    path('history/<int:pk>/', views.AssessmentDetailView.as_view(), name='assessment_detail'),
   
    path('history/<int:pk>/delete/', views.AssessmentDeleteView.as_view(), name='assessment_delete'),
]
