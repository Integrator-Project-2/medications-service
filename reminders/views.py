from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import MedicationReminder
from .serializers import MedicationReminderSerializer
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
