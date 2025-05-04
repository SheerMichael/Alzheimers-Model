# alzheimers_app/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import AlzheimersForm
from .models import PredictionResult
from ml.predictor import predict

def home(request):
    """Home page view"""
    return render(request, 'alzheimers_app/home.html')

def prediction_form(request):
    """View for the prediction form and results"""
    if request.method == 'POST':
        form = AlzheimersForm(request.POST)
        if form.is_valid():
            # Extract data from form
            age = form.cleaned_data['age']
            gender = int(form.cleaned_data['gender'])
            education = form.cleaned_data['education']
            mmse = form.cleaned_data['mmse']
            
            # Create feature array (update to match your model's expected features)
            features = [age, gender, education, mmse]
            
            try:
                # Get prediction
                result = predict(features)
                
                # Interpret prediction
                prediction = result.get('prediction')
                probability = result.get('probability')
                
                # Save to database (optional)
                PredictionResult.objects.create(
                    age=age,
                    gender=gender,
                    education=education,
                    mmse=mmse,
                    prediction=prediction,
                    probability=probability if probability else None
                )
                
                # Map prediction code to meaningful label
                prediction_labels = {
                    0: "Non-Demented",
                    1: "Mild Dementia", 
                    2: "Moderate Dementia",
                    3: "Severe Dementia"
                }
                prediction_label = prediction_labels.get(prediction, f"Unknown ({prediction})")
                
                # Pass results to template
                return render(request, 'alzheimers_app/result.html', {
                    'prediction': prediction,
                    'prediction_label': prediction_label,
                    'probability': probability,
                    'input_data': {
                        'Age': age,
                        'Gender': 'Male' if gender == 1 else 'Female',
                        'Education': education,
                        'MMSE Score': mmse
                    }
                })
                
            except Exception as e:
                messages.error(request, f"Prediction error: {str(e)}")
                return render(request, 'alzheimers_app/prediction_form.html', {'form': form})
    else:
        form = AlzheimersForm()
    
    return render(request, 'alzheimers_app/prediction_form.html', {'form': form})

def history(request):
    """View for prediction history"""
    predictions = PredictionResult.objects.all().order_by('-created_at')
    return render(request, 'alzheimers_app/history.html', {'predictions': predictions})