from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from .models import MedicationReminder

@receiver(post_save, sender=MedicationReminder)
def create_medication_reminder_records(sender, instance, created, **kwargs):
    if created:
        instance.create_reminder_records()
