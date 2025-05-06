from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views import View
from django.views.generic import ListView, DetailView
from django.http import JsonResponse

from .models import AlzheimersData
from .forms import AlzheimersDataForm
from .predictor import AlzheimersPredictor

class AlzheimersInputView(View):
    """View for inputting patient data and making predictions"""
    
    template_name = 'ml/input_form.html'
    
    def get(self, request):
        form = AlzheimersDataForm()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        form = AlzheimersDataForm(request.POST)
        if form.is_valid():
            # Save form but don't commit to database yet
            instance = form.save(commit=False)
            
            try:
                # Make prediction
                predictor = AlzheimersPredictor()
                result = predictor.predict(instance)
                
                # Update instance with prediction results
                instance.prediction = result['prediction']
                instance.prediction_probability = result.get('probability')
                
                # Save to database
                instance.save()
                
                # Success message
                messages.success(request, f"Prediction complete: {result['prediction']}")
                
                # Redirect to result page
                return redirect('alzheimers_result', pk=instance.pk)
            
            except Exception as e:
                messages.error(request, f"Prediction error: {str(e)}")
                return render(request, self.template_name, {'form': form, 'error': str(e)})
        else:
            return render(request, self.template_name, {'form': form})

class AlzheimersResultView(DetailView):
    """View for displaying prediction results"""
    
    model = AlzheimersData
    template_name = 'ml/result.html'
    context_object_name = 'result'

class AlzheimersHistoryView(ListView):
    """View for displaying history of predictions"""
    
    model = AlzheimersData
    template_name = 'ml/history.html'
    context_object_name = 'predictions'
    ordering = ['-created_at']
    paginate_by = 10

class AlzheimersAPIView(View):
    """API view for making predictions programmatically"""
    
    def post(self, request):
        try:
            # Get data from request
            data = request.POST.dict()
            
            # Convert boolean fields from string to actual boolean
            boolean_fields = [
                'smoking', 'family_history_alzheimers', 'cardiovascular_disease',
                'diabetes', 'depression', 'head_injury', 'hypertension',
                'memory_complaints', 'behavioral_problems', 'confusion',
                'disorientation', 'personality_changes', 'difficulty_completing_tasks',
                'forgetfulness'
            ]
            
            for field in boolean_fields:
                if field in data:
                    data[field] = data[field].lower() in ['true', '1', 'yes', 'y']
            
            # Make prediction
            predictor = AlzheimersPredictor()
            result = predictor.predict(data)
            
            # Return result as JSON
            return JsonResponse({
                'success': True,
                'prediction': result['prediction'],
                'probability': result.get('probability'),
                'timestamp': timezone.now().isoformat()
            })
        
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=400)