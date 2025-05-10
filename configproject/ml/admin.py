from django.contrib import admin
from .models import Assessment

@admin.register(Assessment)
class AssessmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'age', 'get_gender_display', 'result', 'probability', 'date')
    list_filter = ('result', 'gender')
    search_fields = ('user__username', 'user__email')
    date_hierarchy = 'date'
    readonly_fields = ('date', 'result', 'probability', 'data')