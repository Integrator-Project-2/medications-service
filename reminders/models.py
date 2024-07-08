from django.db import models
from medications.models import Medication
from django.core.exceptions import ValidationError
from datetime import datetime, timedelta

class MedicationReminder(models.Model):
    REMINDER_TYPE = [
        ('daily reminder', 'Daily Reminder'),
        ('unique reminder', 'Unique Reminder'),
    ]
    medication = models.ForeignKey(Medication, on_delete=models.DO_NOTHING, blank=True)
    patient = models.IntegerField(null=True, blank=True)
    reminder_type = models.CharField(max_length=20, choices=REMINDER_TYPE, blank=True)
    frequency_per_day = models.IntegerField(default=1, blank=True)
    frequency_hours = models.IntegerField(default=0, null=True, blank=True)
    remind_time = models.TimeField(blank=True)
    day = models.DateField(blank=True)
    medication_taken = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.medication} - {self.reminder_type} on {self.day} at {self.remind_time}"

    def create_reminders(self):
        reminders = []
        
        if self.reminder_type == 'unique reminder' or self.frequency_per_day == 1:
            reminder = MedicationReminder.objects.create(
                medication=self.medication,
                patient=self.patient,
                reminder_type=self.reminder_type,
                remind_time=self.remind_time,
                day=self.day
            )
            reminders.append(reminder)
        elif self.reminder_type == 'daily reminder':

            start_datetime = datetime.combine(self.day, self.remind_time)
            
            for i in range(self.frequency_per_day):
                remind_datetime = start_datetime + timedelta(hours=i * self.frequency_hours)
                reminder = MedicationReminder.objects.create(
                    medication=self.medication,
                    patient=self.patient,
                    reminder_type=self.reminder_type,
                    remind_time=remind_datetime.time(),
                    day=self.day
                )
                reminders.append(reminder)
    
        return reminders


class AmountReminder(models.Model):
    medication = models.OneToOneField(Medication, on_delete=models.DO_NOTHING, blank=True)
    amount = models.IntegerField(blank=True)
    reminder_quantity = models.IntegerField(default=5, blank=True)
    low_stock = models.BooleanField(default=False, blank=True)

    def clean(self):
        if self.medication.pharmaceutical_form not in ['tablet', 'capsule', 'injectable']:
            raise ValidationError({'medication': 'Amount reminders can only be created for tablet, capsule, or injectable medications.'})
        if self.amount <= 0:
            raise ValidationError({'amount': 'Medication amount must be greater than zero.'})
        if self.reminder_quantity < 0:
            raise ValidationError({'reminder_quantity': 'Medication reminder quantity must be greater than or equal to zero.'})

    def save(self, *args, **kwargs):
        if self.amount <= self.reminder_quantity:
            self.low_stock = True
        else:
            self.low_stock = False
        
        self.clean()
        super().save(*args, **kwargs)
