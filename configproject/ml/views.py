from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import FormView, TemplateView
from django.urls import reverse_lazy
from .forms import MCIDetectionForm
from .predictor import MCIPredictor
import logging

logger = logging.getLogger(__name__)

class PredictionFormView(FormView):
    """View for displaying and processing the MCI prediction form"""
    template_name = 'ml/input_form.html'
    form_class = MCIDetectionForm
    success_url = reverse_lazy('ml:prediction_result')
    
    def form_valid(self, form):
        logger.info("FORM VALID – running prediction")
        data = form.cleaned_data
        self.request.session['form_data'] = data
        
        try:
            predictor = MCIPredictor()
            prediction, probability = predictor.predict(data)
            
            self.request.session['prediction'] = int(prediction)
            self.request.session['probability'] = float(probability)
            
            return super().form_valid(form)
            
        except Exception as e:
            messages.error(self.request, f"Prediction error: {str(e)}")
            logger.exception("Prediction error occurred")
            return self.form_invalid(form)

    def form_invalid(self, form):
        logger.warning("FORM INVALID – errors: %s", form.errors)
        return super().form_invalid(form)


class PredictionResultView(TemplateView):
    template_name = 'ml/result.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['result'] = self.request.session.get('prediction', None)
        probability = self.request.session.get('probability', 0)
        context['prob'] = f"{probability:.2%}" if probability is not None else "N/A"
        return context
