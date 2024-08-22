from celery import shared_task
from datetime import timedelta
from django.utils.timezone import localdate
from .models import MedicationReminder

@shared_task
def create_daily_reminders():
    today = localdate()
    tomorrow = today + timedelta(days=1)

    daily_reminders_today = MedicationReminder.objects.filter(reminder_type='daily reminder', day=today)

    for reminder in daily_reminders_today:

        existing_reminder_tomorrow = MedicationReminder.objects.filter(
            medication=reminder.medication,
            patient=reminder.patient,
            reminder_type=reminder.reminder_type,
            remind_time=reminder.remind_time,
            day=tomorrow
        ).exists()

        if not existing_reminder_tomorrow:
            new_reminder = MedicationReminder(
                medication=reminder.medication,
                patient=reminder.patient,
                reminder_type=reminder.reminder_type,
                frequency_per_day=reminder.frequency_per_day,
                frequency_hours=reminder.frequency_hours,
                remind_time=reminder.remind_time,
                day=tomorrow
            )
            new_reminder.save()
