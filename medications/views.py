from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets, status
from .serializers import MedicationSerializer
from medications.models import Medication

class MedicationViewSet(viewsets.ModelViewSet):
    queryset = Medication.objects.all()
    serializer_class = MedicationSerializer
