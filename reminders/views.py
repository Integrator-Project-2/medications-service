from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from .models import AmountReminder, MedicationReminder, MedicationReminderRecord
from .serializers import AmountReminderSerializer, MedicationReminderRecordSerializer, MedicationReminderSerializer
from django.utils.timezone import localdate, localtime, now
from rest_framework.decorators import action
from django.db.models import Q


class CustomRemindersPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
class MedicationReminderViewSet(viewsets.ModelViewSet):
    queryset = MedicationReminder.objects.all()
    serializer_class = MedicationReminderSerializer
    permission_classes = [CustomRemindersPermission]

    def get_queryset(self):
        patient_id = self.request.user.id
        return self.queryset.filter(patient=patient_id) # retorna os lembretes do usuario logado
    
    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def partial_update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    @action(detail=False, methods=['get'], url_path='upcoming')
    def upcoming_reminder(self, request):
        patient_id = self.request.user.id
        current_date = localdate()
        current_time = localtime(now()).time()

        upcoming_reminder = self.get_queryset().filter(
            patient=patient_id,
            day__gte=current_date
        ).filter(
            Q(day=current_date, remind_time__gte=current_time) | Q(day__gt=current_date)
        ).order_by('day', 'remind_time').first()
        
        print(current_date)

        if upcoming_reminder:
            serializer = self.get_serializer(upcoming_reminder)
            return Response(serializer.data)
        else:
            return Response({"detail": "No upcoming reminders found."}, status=status.HTTP_404_NOT_FOUND)


class AmountReminderViewSet(viewsets.ModelViewSet):
    queryset = AmountReminder.objects.all()
    serializer_class = AmountReminderSerializer
    permission_classes = [CustomRemindersPermission]

    def get_queryset(self):
        patient_id = self.request.user.id
        medication_reminders = MedicationReminder.objects.filter(patient=patient_id).values_list('medication', flat=True)
        return AmountReminder.objects.filter(medication__in=medication_reminders)

class MedicationReminderRecordViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = MedicationReminderRecord.objects.all()
    serializer_class = MedicationReminderRecordSerializer
    permission_classes = [CustomRemindersPermission]

    @action(detail=True, methods=['post'], url_path='take-medication')
    def take_medication(self, request, pk=None):
        try:
            reminder_record = self.get_object()

            if reminder_record.taken:
                return Response(
                    {'error': 'This medication reminder has already been marked as taken.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            try:
                amount_reminder = AmountReminder.objects.get(medication=reminder_record.reminder.medication)
                if amount_reminder.amount > 0:
                    amount_reminder.amount -= amount_reminder.quantity_taken
                    amount_reminder.save()
                
                # se o estoque estiver vazio ou negativo após o decremento, retorna uma mensagem de aviso
                if amount_reminder.amount <= 0:
                    warning_message = 'The medication stock is empty. Please refill the stock.'
                    reminder_record.taken = True
                    reminder_record.save()
                    serializer = self.get_serializer(reminder_record)
                    return Response(
                        {'reminder': serializer.data, 'warning': warning_message},
                        status=status.HTTP_200_OK
                    )

            except AmountReminder.DoesNotExist:
                # se não existir AmountReminder apenas marca o lembrete como "tomado"
                pass

            reminder_record.taken = True
            reminder_record.save()

            serializer = self.get_serializer(reminder_record)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except MedicationReminderRecord.DoesNotExist:
            return Response({'error': 'Medication Reminder Record not found'}, status=status.HTTP_404_NOT_FOUND)
