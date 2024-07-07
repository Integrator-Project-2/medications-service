from celery import shared_task
from django.utils import timezone
from reminders.models import MedicationReminder
from datetime import timedelta

@shared_task
def create_daily_reminders():
    today = timezone.now().date()
    tomorrow = today + timedelta(days=1)

    if not MedicationReminder.objects.filter(reminder_type='daily reminder', day=tomorrow).exists():
        daily_reminders = MedicationReminder.objects.filter(reminder_type='daily reminder', day=today)

        for reminder in daily_reminders:
            reminder.medication_taken = False
            reminder.save()

            reminder.create_reminders()