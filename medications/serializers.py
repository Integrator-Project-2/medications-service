from rest_framework import serializers
from medications.models import Medication
from reminders.models import AmountReminder

class MedicationSerializer(serializers.ModelSerializer):
    amount = serializers.SerializerMethodField()
    class Meta:
        model = Medication
        fields = ['id', 'name', 'pharmaceutical_form', 'amount']

    def get_amount(self, obj):
        amount_reminder = AmountReminder.objects.filter(medication=obj).first()
        if amount_reminder:
            return amount_reminder.amount
        return None