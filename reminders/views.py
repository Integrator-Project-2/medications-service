from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from .models import AmountReminder, MedicationReminder
from .serializers import AmountReminderSerializer, MedicationReminderSerializer
from django.utils import timezone
from rest_framework.decorators import action
from datetime import timedelta
from django.utils.timezone import localtime

class CustomRemindersPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
class MedicationReminderViewSet(viewsets.ModelViewSet):
    queryset = MedicationReminder.objects.all()
    serializer_class = MedicationReminderSerializer
    permission_classes = [CustomRemindersPermission]

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
    

    @action(detail=False, methods=['get'])
    def due_reminders(self, request):
        patient_id = request.query_params.get('patient_id')
        if not patient_id:
            return Response({'error': 'Patient ID is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        now = localtime(timezone.now())
        time_range_end = now + timedelta(hours=6)

        reminders = MedicationReminder.objects.filter(
            patient=patient_id,
            day=now.date(),
            remind_time__gte=now.time(),
            remind_time__lte= time_range_end.time(),
            medication_taken=False
        )


        serializer = self.get_serializer(reminders, many=True)
        return Response(serializer.data)

class AmountReminderViewSet(viewsets.ModelViewSet):
    queryset = AmountReminder.objects.all()
    serializer_class = AmountReminderSerializer
    permission_classes = [CustomRemindersPermission]

class TakeMedicationViewSet(viewsets.ViewSet):
    
    permission_classes = [CustomRemindersPermission]
    
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

        low_stock = amount_reminder.low_stock
        
        return Response({'message': 'Medication marked as taken and amount decremented successfully.', 'low_stock': low_stock}, status=status.HTTP_200_OK)
        