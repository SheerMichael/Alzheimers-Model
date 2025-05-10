from django.db import models
from django.contrib.auth.models import User
import json

class Assessment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    age = models.IntegerField()
    gender = models.IntegerField(choices=[(0, 'Male'), (1, 'Female')])
    result = models.BooleanField()  # True = MCI detected, False = No MCI
    probability = models.FloatField()
    data = models.JSONField()
    
    def __str__(self):
        return f"Assessment {self.id} - {'MCI' if self.result else 'No MCI'}"
    
    def get_gender_display(self):
        return 'Male' if self.gender == 0 else 'Female'