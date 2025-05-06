from django import forms
from .models import AlzheimersData

class AlzheimersDataForm(forms.ModelForm):
    """Form for inputting patient data for Alzheimer's prediction"""
    
    # Override some fields for better UX
    ACTIVITY_CHOICES = [
        ('Low', 'Low'),
        ('Moderate', 'Moderate'),
        ('High', 'High'),
    ]
    
    QUALITY_CHOICES = [
        ('Poor', 'Poor'),
        ('Fair', 'Fair'),
        ('Good', 'Good'),
        ('Excellent', 'Excellent'),
    ]
    
    # Lifestyle fields with more user-friendly inputs
    physical_activity = forms.ChoiceField(choices=ACTIVITY_CHOICES)
    diet_quality = forms.ChoiceField(choices=QUALITY_CHOICES)
    sleep_quality = forms.ChoiceField(choices=QUALITY_CHOICES)
    alcohol_consumption = forms.ChoiceField(choices=[
        ('None', 'None'),
        ('Occasional', 'Occasional'),
        ('Moderate', 'Moderate'),
        ('Heavy', 'Heavy'),
    ])
    
    class Meta:
        model = AlzheimersData
        exclude = ['prediction', 'prediction_probability', 'created_at']
        widgets = {
            'patient_id': forms.TextInput(attrs={'placeholder': 'Optional'}),
            'age': forms.NumberInput(attrs={'min': 0, 'max': 120}),
            'education_level': forms.NumberInput(attrs={'min': 0, 'max': 30}),
            'bmi': forms.NumberInput(attrs={'step': '0.1', 'min': 10, 'max': 50}),
            'systolic_bp': forms.NumberInput(attrs={'min': 80, 'max': 220}),
            'diastolic_bp': forms.NumberInput(attrs={'min': 40, 'max': 120}),
            'cholesterol_total': forms.NumberInput(attrs={'step': '0.1', 'min': 100, 'max': 500}),
            'cholesterol_ldl': forms.NumberInput(attrs={'step': '0.1', 'min': 0, 'max': 300}),
            'cholesterol_hdl': forms.NumberInput(attrs={'step': '0.1', 'min': 0, 'max': 100}),
            'cholesterol_triglycerides': forms.NumberInput(attrs={'step': '0.1', 'min': 0, 'max': 1000}),
            'mmse': forms.NumberInput(attrs={'min': 0, 'max': 30}),
            'functional_assessment': forms.NumberInput(attrs={'min': 0, 'max': 100}),
            'adl': forms.NumberInput(attrs={'min': 0, 'max': 100}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make most fields required
        for field_name, field in self.fields.items():
            # Except for these fields
            if field_name not in ['patient_id', 'ethnicity', 'doctor_in_charge', 'actual_diagnosis']:
                field.required = True