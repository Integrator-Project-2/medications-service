from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from .models import AmountReminder, MedicationReminder
from .serializers import AmountReminderSerializer, MedicationReminderSerializer
from django.utils import timezone
from rest_framework.decorators import action
from datetime import timedelta
from django.utils.timezone import localtime

# class CustomRemindersPermission(permissions.BasePermission):
#     def has_permission(self, request, view):
#         return request.user and request.user.is_authenticated
class MedicationReminderViewSet(viewsets.ModelViewSet):
    queryset = MedicationReminder.objects.all()
    serializer_class = MedicationReminderSerializer
    # permission_classes = [CustomRemindersPermission]

    def get_queryset(self):
        patient_id = self.request.user.id
        return self.queryset.filter(patient=patient_id) # retorna os lembretes do usuario logado
    
    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def partial_update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

class AmountReminderViewSet(viewsets.ModelViewSet):
    queryset = AmountReminder.objects.all()
    serializer_class = AmountReminderSerializer
    # permission_classes = [CustomRemindersPermission]

class TakeMedicationViewSet(viewsets.ViewSet):
    
    # permission_classes = [CustomRemindersPermission]
    
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
        