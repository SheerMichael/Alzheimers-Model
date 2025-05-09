from django.conf import settings
from django.db import models

class PredictionRecord(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    # paste all your MCIDetectionForm fields here:
    Age = models.IntegerField()
    Gender = models.IntegerField()
    Ethnicity = models.IntegerField()
    EducationLevel = models.IntegerField()
    BMI = models.FloatField()
    Smoking = models.IntegerField()
    AlcoholConsumption = models.IntegerField()
    PhysicalActivity = models.IntegerField()
    DietQuality = models.IntegerField()
    SleepQuality = models.IntegerField()
    FamilyHistoryAlzheimers = models.IntegerField()
    CardiovascularDisease = models.IntegerField()
    Diabetes = models.IntegerField()
    Depression = models.IntegerField()
    HeadInjury = models.IntegerField()
    Hypertension = models.IntegerField()

    result = models.BooleanField()       # True = MCI
    probability = models.FloatField()

    def __str__(self):
        return f"{self.user or 'Anon'} – {self.timestamp:%Y-%m-%d %H:%M}"
