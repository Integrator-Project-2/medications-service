from rest_framework import serializers
from medications.models import Medication

class MedicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medication
        fields = ['id', 'name', 'pharmaceutical_form']
