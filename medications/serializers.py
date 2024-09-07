from rest_framework import serializers
from medications.models import Medication
from reminders.models import AmountReminder

class MedicationSerializer(serializers.ModelSerializer):
    amount = serializers.SerializerMethodField()
    low_stock = serializers.SerializerMethodField()
    class Meta:
        model = Medication
        fields = ['id', 'name', 'pharmaceutical_form', 'amount', 'low_stock']

    def get_amount(self, obj):
        amount_reminder = AmountReminder.objects.filter(medication=obj).first()
        if amount_reminder:
            return amount_reminder.amount
        return None
 
    def get_low_stock(self, obj):
        amount_reminder = AmountReminder.objects.filter(medication=obj).first()
        if amount_reminder:
            return amount_reminder.low_stock
        return None