from django.contrib import admin
from reminders.models import MedicationReminder, MedicationReminderRecord

# Register your models here.
admin.site.register(MedicationReminder)
admin.site.register(MedicationReminderRecord)