# alzheimers_app/forms.py
from django import forms

class AlzheimersForm(forms.Form):
    """
    Form for Alzheimer's prediction inputs
    
    Note: Update these fields based on your actual model features
    """
    age = forms.IntegerField(
        min_value=0, 
        max_value=120,
        help_text="Patient's age in years"
    )
    
    gender = forms.ChoiceField(
        choices=[
            (0, 'Female'),
            (1, 'Male')
        ],
        help_text="Patient's gender"
    )
    
    education = forms.IntegerField(
        min_value=0,
        max_value=30,
        help_text="Years of education"
    )
    
    mmse = forms.FloatField(
        min_value=0,
        max_value=30,
        help_text="Mini-Mental State Examination score (0-30)"
    )
    
    # Add any other features your model needs
    # Example:
    # brain_volume = forms.FloatField(
    #     help_text="Brain volume measurement"
    # )