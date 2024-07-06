from rest_framework import serializers
from .models import MedicationReminder

class MedicationReminderSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicationReminder
        fields = ['id', 'medication', 'patient', 'reminder_type',  'frequency_per_day', 'frequency_hours', 'remind_time', 'day']
