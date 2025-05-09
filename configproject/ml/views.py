from django.shortcuts import render
from django.views import View
from .forms import MCIDetectionForm
from .predictor import MCIPredictor

class PredictionFormView(View):
    template_name = 'ml/input_form.html'

    def get(self, request):
        return render(request, self.template_name, {'form': MCIDetectionForm()})

    def post(self, request):
        form = MCIDetectionForm(request.POST)
        if not form.is_valid():
            return render(request, self.template_name, {'form': form})

        print("Cleaned form data:", form.cleaned_data)  # ✅ Move it here

        pred, prob = MCIPredictor().predict(form.cleaned_data)
        return render(request, 'ml/result.html', {'result': pred, 'prob': f"{prob:.0%}"})