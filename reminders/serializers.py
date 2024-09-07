from rest_framework import serializers

from medications.models import Medication
from medications.serializers import MedicationSerializer
from .models import AmountReminder, MedicationReminder, MedicationReminderRecord

class MedicationReminderSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicationReminder
        fields = ['id', 'medication', 'patient', 'reminder_type',  'frequency_per_day', 'frequency_hours', 'remind_time', 'day']

class MedicationReminderDetailSerializer(serializers.ModelSerializer):

    medication = MedicationSerializer()
    class Meta:
        model = MedicationReminder
        fields = ['id', 'medication', 'patient', 'reminder_type', 'frequency_per_day', 'frequency_hours', 'remind_time', 'day']

class AmountReminderSerializer(serializers.ModelSerializer):
    class Meta:
        model = AmountReminder
        fields = ['id', 'medication', 'amount', 'reminder_quantity', 'low_stock', 'quantity_taken']

class MedicationReminderRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicationReminderRecord
        fields = ['id', 'reminder', 'date', 'remind_time', 'taken']