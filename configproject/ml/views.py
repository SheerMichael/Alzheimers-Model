from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.utils import timezone
from django.db.models import Count
from .forms import MCIDetectionForm
from .predictor import MCIPredictor
from .models import Assessment
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

class DashboardView(LoginRequiredMixin, View):
    template_name = 'ml/dashboard.html'
    login_url = 'login'

    def get(self, request):
        total = Assessment.objects.count()
        mci = Assessment.objects.filter(result=True).count()
        recent = Assessment.objects.order_by('-date')[:10]
        return render(request, self.template_name, {
            'total_patients': total,
            'mci_count': mci,
            'recent_assessments': recent,
        })

class PredictionFormView(View):
    template_name = 'ml/input_form.html'

    def get(self, request):
        return render(request, self.template_name, {'form': MCIDetectionForm()})

    def post(self, request):
        form = MCIDetectionForm(request.POST)
        if not form.is_valid():
            return render(request, self.template_name, {'form': form})

        print("Cleaned form data:", form.cleaned_data)

        pred, prob = MCIPredictor().predict(form.cleaned_data)
        return render(request, 'ml/result.html', {'result': pred, 'prob': f"{prob:.0%}"})

class AssessmentListView(LoginRequiredMixin, ListView):
    model = Assessment
    template_name = 'ml/assessment_list.html'
    context_object_name = 'assessments'
    paginate_by = 20

class AssessmentDetailView(LoginRequiredMixin, DetailView):
    model = Assessment
    template_name = 'ml/assessment_detail.html'
    context_object_name = 'assessment'

class AssessmentDeleteView(LoginRequiredMixin, DeleteView):
    model = Assessment
    template_name = 'ml/assessment_confirm_delete.html'
    success_url = reverse_lazy('assessment_history')
