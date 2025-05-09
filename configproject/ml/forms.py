from django import forms

class MCIDetectionForm(forms.Form):
    # Demographics
    Age = forms.IntegerField(min_value=0, max_value=120, required=True)
    GENDER_CHOICES = [
        (0, 'Female'),
        (1, 'Male'),
    ]
    Gender = forms.ChoiceField(choices=GENDER_CHOICES, required=True)
    
    # Education
    EDUCATION_CHOICES = [
        (0, 'No formal education'),
        (1, 'Primary school'),
        (2, 'High school'),
        (3, 'Bachelor\'s degree'),
        (4, 'Master\'s degree or higher'),
    ]
    EducationLevel = forms.ChoiceField(choices=EDUCATION_CHOICES, required=True)
    
    # Physical measurements
    BMI = forms.FloatField(min_value=10, max_value=50, required=True, 
                          help_text='Body Mass Index')
    
    # Lifestyle factors
    SMOKING_CHOICES = [
        (0, 'Never smoked'),
        (1, 'Former smoker'),
        (2, 'Current smoker'),
    ]
    Smoking = forms.ChoiceField(choices=SMOKING_CHOICES, required=True)
    
    ALCOHOL_CHOICES = [
        (0, 'Never'),
        (1, 'Occasionally'),
        (2, 'Moderate'),
        (3, 'Heavy'),
    ]
    AlcoholConsumption = forms.ChoiceField(choices=ALCOHOL_CHOICES, required=True)
    
    ACTIVITY_CHOICES = [
        (0, 'Sedentary'),
        (1, 'Light'),
        (2, 'Moderate'),
        (3, 'Vigorous'),
    ]
    PhysicalActivity = forms.ChoiceField(choices=ACTIVITY_CHOICES, required=True)
    
    QUALITY_CHOICES = [
        (0, 'Poor'),
        (1, 'Fair'),
        (2, 'Good'),
        (3, 'Excellent'),
    ]
    DietQuality = forms.ChoiceField(choices=QUALITY_CHOICES, required=True)
    SleepQuality = forms.ChoiceField(choices=QUALITY_CHOICES, required=True)
    
    # Medical history - binary choices
    BINARY_CHOICES = [
        (0, 'No'),
        (1, 'Yes'),
    ]
    FamilyHistoryAlzheimers = forms.ChoiceField(choices=BINARY_CHOICES, required=True,
                                              label='Family History of Alzheimer\'s')
    CardiovascularDisease = forms.ChoiceField(choices=BINARY_CHOICES, required=True)
    Diabetes = forms.ChoiceField(choices=BINARY_CHOICES, required=True)
    Depression = forms.ChoiceField(choices=BINARY_CHOICES, required=True)
    HeadInjury = forms.ChoiceField(choices=BINARY_CHOICES, required=True,
                                 label='History of Head Injury')
    Hypertension = forms.ChoiceField(choices=BINARY_CHOICES, required=True)
    
    def clean(self):
        """Convert string values to appropriate numeric types for the model"""
        cleaned_data = super().clean()
        for field in self.fields:
            if field in cleaned_data and field != 'Age' and field != 'BMI':
                cleaned_data[field] = int(cleaned_data[field])
        
        return cleaned_data