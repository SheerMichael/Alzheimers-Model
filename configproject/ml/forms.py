from django import forms
from .models import Assessment

class MCIDetectionForm(forms.Form):
    # Demographics
    Age = forms.IntegerField(min_value=60, max_value=90)
    Gender = forms.ChoiceField(choices=[(0, 'Male'), (1, 'Female')])
    Ethnicity = forms.ChoiceField(choices=[
        (0, 'Caucasian'), (1, 'African American'), (2, 'Asian'), (3, 'Other')
    ])

    # Education level
    EducationLevel = forms.ChoiceField(choices=[
        (0, 'None'), (1, 'High School'), (2, "Bachelor's"), (3, 'Higher')
    ])

    # Measurements & lifestyle
    BMI = forms.FloatField(min_value=15, max_value=40)
    Smoking = forms.ChoiceField(choices=[(0, 'No'), (1, 'Yes')])
    AlcoholConsumption = forms.IntegerField(min_value=0, max_value=20)
    PhysicalActivity = forms.IntegerField(min_value=0, max_value=10)
    DietQuality = forms.IntegerField(min_value=0, max_value=10)
    SleepQuality = forms.IntegerField(min_value=4, max_value=10)

    # Medical history
    FamilyHistoryAlzheimers = forms.ChoiceField(choices=[(0, 'No'), (1, 'Yes')])
    CardiovascularDisease   = forms.ChoiceField(choices=[(0, 'No'), (1, 'Yes')])
    Diabetes                = forms.ChoiceField(choices=[(0, 'No'), (1, 'Yes')])
    Depression              = forms.ChoiceField(choices=[(0, 'No'), (1, 'Yes')])
    HeadInjury              = forms.ChoiceField(choices=[(0, 'No'), (1, 'Yes')])
    Hypertension            = forms.ChoiceField(choices=[(0, 'No'), (1, 'Yes')])

    def clean(self):
        data = super().clean()
        for k, v in data.items():
            if k not in ('Age', 'BMI') and v is not None:
                data[k] = int(v)
        return data

