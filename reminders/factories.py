from datetime import timedelta, datetime
from django.utils.timezone import localdate
from abc import ABC, abstractmethod

class ReminderFactory(ABC):
    @abstractmethod
    def create_reminder(self, reminder):
        pass

    
class DailyReminderFactory(ReminderFactory):
    def create_reminder(self, reminder):
       
        from reminders.models import MedicationReminderRecord
        
        today = localdate()
        start_time = datetime.combine(today, reminder.remind_time)
        for i in range(reminder.frequency_per_day):
            if reminder.frequency_hours is not None and reminder.frequency_hours > 0:
                remind_time = start_time + timedelta(hours=i * reminder.frequency_hours)
                remind_date = remind_time.date()
                MedicationReminderRecord.objects.get_or_create(
                    reminder=reminder,
                    date=remind_date,
                    remind_time=remind_time.time()
                )

class UniqueReminderFactory(ReminderFactory):
    def create_reminder(self, reminder):

        from reminders.models import MedicationReminderRecord
        
        MedicationReminderRecord.objects.get_or_create(
            reminder=reminder,
            date=reminder.day,
            remind_time=reminder.remind_time
        )


FACTORY_MAP = {
    'daily reminder': DailyReminderFactory(),
    'unique reminder': UniqueReminderFactory(),
}
