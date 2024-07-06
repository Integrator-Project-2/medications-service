# Generated by Django 5.0.4 on 2024-07-05 18:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('medications', '0002_remove_medication_patient_id_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='MedicationReminder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('patient', models.IntegerField(blank=True, null=True)),
                ('reminder_type', models.CharField(choices=[('daily reminder', 'Daily Reminder'), ('unique reminder', 'Unique Reminder')], max_length=20)),
                ('frequency_per_day', models.IntegerField(default=1)),
                ('frequency_hours', models.IntegerField(blank=True, default=1, null=True)),
                ('remind_time', models.TimeField()),
                ('day', models.DateField(auto_now_add=True)),
                ('medication_taken', models.BooleanField(default=False)),
                ('medication', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='medications.medication')),
            ],
        ),
    ]
