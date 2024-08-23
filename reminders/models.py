from datetime import timedelta, datetime
from django.utils.timezone import localdate
from django.db import models
from medications.models import Medication
from django.core.exceptions import ValidationError

class MedicationReminder(models.Model):
    REMINDER_TYPE = [
        ('daily reminder', 'Daily Reminder'),
        ('unique reminder', 'Unique Reminder'),
    ]
    medication = models.ForeignKey(Medication, on_delete=models.DO_NOTHING, blank=True)
    patient = models.IntegerField(null=True, blank=True)
    reminder_type = models.CharField(max_length=20, choices=REMINDER_TYPE, blank=True)
    frequency_per_day = models.IntegerField(default=1, blank=True, null=True)
    frequency_hours = models.IntegerField(default=0, null=True, blank=True)
    remind_time = models.TimeField(blank=True)
    day = models.DateField(blank=True)

    def __str__(self):
        return f"{self.medication} - {self.reminder_type} on {self.day} at {self.remind_time}"

    def clean(self):
        if self.reminder_type == 'unique reminder':
            self.frequency_per_day = None
            self.frequency_hours = None

        elif self.reminder_type == 'daily reminder':

            if self.frequency_per_day <= 0:
                raise ValidationError({'frequency_per_day': 'Frequency per day must be at least 1 for daily reminders.'})
             
            if self.frequency_per_day > 1 and (self.frequency_hours is None or self.frequency_hours <= 0):
                raise ValidationError({'frequency_hours' : 'For reminders more than once per day, frequency hours must be greater than 0'})
    
            if self.frequency_per_day == 1:
                self.frequency_hours = None
    
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def create_reminder_records(self):
        today = localdate()
        start_time = datetime.combine(today, self.remind_time)

        if self.reminder_type == 'unique reminder':
                MedicationReminderRecord.objects.get_or_create(
                    reminder=self,
                    date=self.day,
                    remind_time=self.remind_time
                )
            
        elif self.reminder_type == 'daily reminder':
            if self.frequency_per_day == 1:
                MedicationReminderRecord.objects.get_or_create(
                    reminder=self,
                    date=today,
                    remind_time=self.remind_time
                )
            else:
                for i in range(self.frequency_per_day):
                    if self.frequency_hours is not None and self.frequency_hours > 0:
                        remind_time = start_time + timedelta(hours=i * self.frequency_hours)
                        remind_date = remind_time.date()
                        
                        MedicationReminderRecord.objects.get_or_create(
                            reminder=self,
                            date=remind_date,
                            remind_time=remind_time.time()
                        )
class MedicationReminderRecord(models.Model):
    reminder = models.ForeignKey(MedicationReminder, on_delete=models.CASCADE, related_name="reminder_records")
    date = models.DateField()
    remind_time = models.TimeField()
    taken = models.BooleanField(default=False)

    def __str__(self):
        return f'Reminder for {self.reminder.medication} on {self.date} at {self.remind_time} - Taken: {self.taken}'

class AmountReminder(models.Model):
    medication = models.OneToOneField(Medication, on_delete=models.DO_NOTHING, blank=True)
    amount = models.IntegerField(blank=True)
    reminder_quantity = models.IntegerField(default=5, blank=True)
    quantity_taken = models.IntegerField(default=1)
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
