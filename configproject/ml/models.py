from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class PredictionResult(models.Model):
    """
    Store prediction results for Alzheimer's disease predictions
    """
    # Patient information
    patient_id = models.CharField(max_length=50, blank=True, null=True, help_text="Optional patient identifier")
    
    # Demographic features
    age = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(120)], 
                             help_text="Patient age in years")
    GENDER_CHOICES = [(0, 'Male'), (1, 'Female')]
    gender = models.IntegerField(choices=GENDER_CHOICES, help_text="Patient gender")
    
    ETHNICITY_CHOICES = [
        (0, 'Caucasian'),
        (1, 'African American'),
        (2, 'Hispanic'),
        (3, 'Asian'),
        (4, 'Other')
    ]
    ethnicity = models.IntegerField(choices=ETHNICITY_CHOICES, null=True, blank=True)
    
    EDUCATION_CHOICES = [
        (0, 'Less than high school'),
        (1, 'High school'),
        (2, 'Some college'),
        (3, 'Bachelor degree'),
        (4, 'Graduate degree')
    ]
    education_level = models.IntegerField(choices=EDUCATION_CHOICES)
    
    # Health metrics
    bmi = models.FloatField(validators=[MinValueValidator(10), MaxValueValidator(100)], 
                           null=True, blank=True, help_text="Body Mass Index")
    
    # Risk factors
    smoking = models.BooleanField(default=False)
    alcohol_consumption = models.BooleanField(default=False)
    family_history_alzheimers = models.BooleanField(default=False)
    
    # Medical conditions
    cardiovascular_disease = models.BooleanField(default=False)
    diabetes = models.BooleanField(default=False)
    depression = models.BooleanField(default=False)
    hypertension = models.BooleanField(default=False)
    head_injury = models.BooleanField(default=False)
    
    # Clinical measurements
    systolic_bp = models.IntegerField(null=True, blank=True)
    diastolic_bp = models.IntegerField(null=True, blank=True)
    
    # Cognitive assessments
    mmse = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(30)], 
                            help_text="Mini-Mental State Examination score (0-30)")
    
    # Symptoms
    memory_complaints = models.BooleanField(default=False)
    behavioral_problems = models.BooleanField(default=False)
    adl = models.FloatField(null=True, blank=True, help_text="Activities of Daily Living score")
    confusion = models.BooleanField(default=False)
    disorientation = models.BooleanField(default=False)
    
    # Prediction output
    DIAGNOSIS_CHOICES = [
        (0, 'Cognitively Normal'),
        (1, 'Mild Cognitive Impairment'),
        (2, 'Alzheimer\'s Disease')
    ]
    prediction = models.IntegerField(choices=DIAGNOSIS_CHOICES)
    probability = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(100)],
                                   help_text="Confidence percentage for the prediction")
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    doctor_notes = models.TextField(blank=True, null=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Alzheimer's Prediction"
        verbose_name_plural = "Alzheimer's Predictions"
    
    def __str__(self):
        diagnosis = self.get_prediction_display()
        return f"Patient {self.patient_id or self.id}: {diagnosis} ({self.probability:.1f}%) - {self.created_at.strftime('%Y-%m-%d')}"