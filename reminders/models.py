import datetime
from django.db import models
from medications.models import Medication


class MedicationReminder(models.Model):
    REMINDER_TYPE = [
        ('daily reminder', 'Daily Reminder'),
        ('unique reminder', 'Unique Reminder'),
    ]
    
    medication = models.ForeignKey(Medication, on_delete=models.DO_NOTHING)
    patient = models.IntegerField(null=True, blank=True)
    reminder_type = models.CharField(max_length=20, choices=REMINDER_TYPE)
    frequency_per_day = models.IntegerField(default=1)
    frequency_hours = models.IntegerField(default=1, null=True, blank=True)
    remind_time = models.TimeField()
    day = models.DateField(auto_now_add=True)
    medication_taken = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.medication} - {self.reminder_type} on {self.day} at {self.remind_time}"

    def post(self):
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
            start_datetime = datetime.datetime.combine(self.day, self.remind_time)
            
            for i in range(self.frequency_per_day):
                remind_datetime = start_datetime + datetime.timedelta(hours=i * self.frequency_hours)
                reminder = MedicationReminder.objects.create(
                    medication=self.medication,
                    patient=self.patient,
                    reminder_type=self.reminder_type,
                    remind_time=remind_datetime.time(),
                    day=self.day
                )
                reminders.append(reminder)

        return reminders
