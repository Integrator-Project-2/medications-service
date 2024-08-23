from celery import shared_task
from django.utils.timezone import localdate
from .models import MedicationReminder
import logging
logger = logging.getLogger(__name__)

@shared_task
def create_daily_reminders():
    logger.info('Starting create_daily_reminders task')
    reminders = MedicationReminder.objects.filter(reminder_type='daily reminder')
    
    for reminder in reminders:
        logger.info(f'Creating reminder records for: {reminder}')
        reminder.create_reminder_records()
        logger.info("Lembrete diário criado com sucesso")
        
    logger.info('Finished create_daily_reminders task')
