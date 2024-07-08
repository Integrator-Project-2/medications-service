from rest_framework import serializers
from .models import AmountReminder, MedicationReminder

class MedicationReminderSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicationReminder
        fields = ['id', 'medication', 'patient', 'reminder_type',  'frequency_per_day', 'frequency_hours', 'remind_time', 'day', 'medication_taken']

class AmountReminderSerializer(serializers.ModelSerializer):
    class Meta:
        model = AmountReminder
        fields = ['id', 'medication', 'amount', 'reminder_quantity']

