import datetime
from django.core.management import setup_environ
from django.conf import settings

# Configure Django settings
setup_environ(settings)

from medications.models import MedicationReminder

def create_daily_reminders():
    # Obter todos os lembretes que são 'daily reminders'
    daily_reminders = MedicationReminder.objects.filter(reminder_type='daily reminder')

    new_reminders = []
    for reminder in daily_reminders:
        # Calcular a data do próximo dia
        tomorrow = datetime.date.today() + datetime.timedelta(days=1)

        # Criar um novo lembrete para o próximo dia no mesmo horário
        new_reminder = MedicationReminder.objects.create(
            medication=reminder.medication,
            patient=reminder.patient,
            reminder_type='daily reminder',
            frequency_per_day=reminder.frequency_per_day,
            frequency_hours=reminder.frequency_hours,
            remind_time=reminder.remind_time,
            day=tomorrow,
            medication_taken=False
        )
        new_reminders.append(new_reminder)

    return new_reminders

if __name__ == '__main__':
    created_reminders = create_daily_reminders()
    print(f"Created {len(created_reminders)} daily reminders for tomorrow.")
