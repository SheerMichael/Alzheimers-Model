from django.db import models

class AlzheimersData(models.Model):
    """Model to store patient data and prediction results"""
    
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    
    DIAGNOSIS_CHOICES = [
        ('Positive', 'Alzheimer\'s Positive'),
        ('Negative', 'Alzheimer\'s Negative'),
        ('MCI', 'Mild Cognitive Impairment'),
    ]
    
    # Basic Information
    # patient_id = models.CharField(max_length=50, blank=True)
    age = models.IntegerField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    # ethnicity = models.CharField(max_length=50, blank=True)
    education_level = models.IntegerField(help_text="Years of education")
    bmi = models.FloatField(verbose_name="BMI")
    
    # Lifestyle Factors
    smoking = models.BooleanField(default=False)
    alcohol_consumption = models.CharField(max_length=20, blank=True)
    physical_activity = models.CharField(max_length=20, blank=True)
    diet_quality = models.CharField(max_length=20, blank=True)
    sleep_quality = models.CharField(max_length=20, blank=True)
    
    # Medical History
    family_history_alzheimers = models.BooleanField(default=False)
    cardiovascular_disease = models.BooleanField(default=False)
    diabetes = models.BooleanField(default=False)
    depression = models.BooleanField(default=False)
    head_injury = models.BooleanField(default=False)
    hypertension = models.BooleanField(default=False)
    
    # Clinical Measurements
    systolic_bp = models.IntegerField(verbose_name="Systolic BP")
    diastolic_bp = models.IntegerField(verbose_name="Diastolic BP")
    cholesterol_total = models.FloatField()
    cholesterol_ldl = models.FloatField(verbose_name="LDL Cholesterol")
    cholesterol_hdl = models.FloatField(verbose_name="HDL Cholesterol")
    cholesterol_triglycerides = models.FloatField()
    
    # Cognitive Assessment
    mmse = models.IntegerField(verbose_name="MMSE Score")
    functional_assessment = models.IntegerField()
    memory_complaints = models.BooleanField(default=False)
    behavioral_problems = models.BooleanField(default=False)
    adl = models.IntegerField(verbose_name="Activities of Daily Living Score")
    confusion = models.BooleanField(default=False)
    disorientation = models.BooleanField(default=False)
    personality_changes = models.BooleanField(default=False)
    difficulty_completing_tasks = models.BooleanField(default=False)
    forgetfulness = models.BooleanField(default=False)
    
    # Result and metadata
    prediction = models.CharField(max_length=20, blank=True)
    prediction_probability = models.FloatField(null=True, blank=True)
    actual_diagnosis = models.CharField(max_length=10, choices=DIAGNOSIS_CHOICES, blank=True, null=True)
    # doctor_in_charge = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Patient {self.patient_id} - {'Prediction' if not self.actual_diagnosis else 'Diagnosis'}: {self.prediction or self.actual_diagnosis}"
    
    class Meta:
        verbose_name = "Alzheimer's Data"
        verbose_name_plural = "Alzheimer's Data"