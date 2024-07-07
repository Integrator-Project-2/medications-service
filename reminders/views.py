from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import AmountReminder, MedicationReminder
from .serializers import AmountReminderSerializer, MedicationReminderSerializer
from django.utils import timezone

class MedicationReminderViewSet(viewsets.ModelViewSet):
    queryset = MedicationReminder.objects.all()
    serializer_class = MedicationReminderSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
    
        validated_data = serializer.validated_data

        reminder = MedicationReminder(
            medication=validated_data['medication'],
            patient=validated_data.get('patient'),
            reminder_type=validated_data['reminder_type'],
            frequency_per_day=validated_data.get('frequency_per_day', 1),
            frequency_hours=validated_data.get('frequency_hours', 1),
            remind_time=validated_data.get('remind_time'),
            day=validated_data.get('day', timezone.now().date())
        )

        reminders = reminder.create_reminders()
      
        reminders_serializer = self.get_serializer(reminders, many=True)
        
        return Response(reminders_serializer.data, status=status.HTTP_201_CREATED)

class AmountReminderViewSet(viewsets.ModelViewSet):
    queryset = AmountReminder.objects.all()
    serializer_class = AmountReminderSerializer

class TakeMedicationViewSet(viewsets.ViewSet):
    
    def update(self, request, pk=None):
        try:
            medication_reminder = MedicationReminder.objects.get(pk=pk)
        except MedicationReminder.DoesNotExist:
            return Response({'error': 'Medication Reminder not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        if medication_reminder.medication_taken:
            return Response({'message': 'Medication already marked as taken.'}, status=status.HTTP_400_BAD_REQUEST)
        
        medication_reminder.medication_taken = True
        medication_reminder.save()
        
        try:
            amount_reminder = AmountReminder.objects.get(medication=medication_reminder.medication)
        except AmountReminder.DoesNotExist:
            return Response({'error': 'Amount Reminder not found for this medication.'}, status=status.HTTP_404_NOT_FOUND)
        
        amount_reminder.amount -= 1
        amount_reminder.save()
        
        return Response({'message': 'Medication marked as taken and amount decremented successfully.'}, status=status.HTTP_200_OK)