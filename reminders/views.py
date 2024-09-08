from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from . import serializers
from .models import AmountReminder, MedicationReminder, MedicationReminderRecord
from django.utils.timezone import localdate, localtime, now
from rest_framework.decorators import action
from django.db.models import Q


class MedicationReminderViewSet(viewsets.ModelViewSet):
    queryset = MedicationReminder.objects.all()
 
    def get_serializer_class(self):
        if self.action == 'retrieve' or self.action == 'list' :
            return serializers.MedicationReminderDetailSerializer
        return serializers.MedicationReminderSerializer

    def get_queryset(self):
        patient_id = self.request.query_params.get('patient_id')
        if patient_id:
            return self.queryset.filter(patient=patient_id).order_by('-day', '-remind_time')
        else:
             return self.queryset.order_by('-day', '-remind_time')
    
    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def partial_update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    def destroy(self, request, *args, **kwargs):
        reminder = self.get_object()
        print(f"Deleting reminder: {reminder}")
        reminder.delete()
        return Response({"detail": "Medication reminder deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

    
    @action(detail=False, methods=['get'], url_path='upcoming')
    def upcoming_reminder(self, request):
        patient_id = self.request.query_params.get('patient_id', self.request.user.id)
        current_date = localdate()
        current_time = localtime(now()).time()

        upcoming_reminder = self.get_queryset().filter(
            patient=patient_id,
            day__gte=current_date
        ).filter(
            Q(day=current_date, remind_time__gte=current_time) | Q(day__gt=current_date)
        ).order_by('day', 'remind_time').first()

        if upcoming_reminder:
            serializer = self.get_serializer(upcoming_reminder)
            return Response(serializer.data)
        else:
            return Response({"detail": "No upcoming reminders found."}, status=status.HTTP_404_NOT_FOUND)


class AmountReminderViewSet(viewsets.ModelViewSet):
    queryset = AmountReminder.objects.all()
    serializer_class = serializers.AmountReminderSerializer

class MedicationReminderRecordViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = MedicationReminderRecord.objects.all()
    serializer_class = serializers.MedicationReminderRecordSerializer

    def get_queryset(self):
        patient_id = self.request.query_params.get('patient_id', None)
        reminder_id = self.request.query_params.get('reminder_id', None)

        queryset = MedicationReminderRecord.objects.all()

        if patient_id:
            queryset = queryset.filter(reminder__patient=patient_id)
        elif reminder_id:
            queryset = queryset.filter(reminder=reminder_id)

        
        queryset = queryset.order_by('-date', '-remind_time')

        return queryset
            
    @action(detail=False, methods=['get'], url_path='upcoming')
    def upcoming_reminders(self, request):
        patient_id = self.request.query_params.get('patient_id', None)

        medication_reminder_ids = MedicationReminder.objects.filter(patient=patient_id).values_list('id', flat=True)

        # filtra lembretes que ainda não foram tomados
        upcoming_reminder = self.queryset.filter(
            reminder__in=medication_reminder_ids,
            taken=False,
           
        ).order_by('date', 'remind_time').first()

        if upcoming_reminder:
            serializer = self.get_serializer(upcoming_reminder) 
         
        return Response(serializer.data, status=status.HTTP_200_OK)

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

                    if amount_reminder.amount < 0:
                        amount_reminder.amount = 0

                    amount_reminder.save()
                
                # se o estoque estiver vazio ou negativo após o decremento, retorna uma mensagem de aviso
                if amount_reminder.amount == 0:
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
