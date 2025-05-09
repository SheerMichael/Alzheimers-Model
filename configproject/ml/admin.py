# ml/admin.py

from django.contrib import admin
from .models import PredictionRecord

@admin.register(PredictionRecord)
class PredictionRecordAdmin(admin.ModelAdmin):
    # make the timestamp read-only
    readonly_fields = ('timestamp',)

    # show columns that actually exist:
    list_display = (
        'user',
        'Age',
        'Gender',
        'Ethnicity',
        'result',
        'probability',
        'timestamp',
    )
    # filters on real model fields:
    list_filter = (
        'result',
        'timestamp',
        'Gender',
        'Ethnicity',
    )
    # let you search by username
    search_fields = ('user__username',)
