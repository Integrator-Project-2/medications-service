# Generated by Django 5.0.4 on 2024-08-22 16:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reminders', '0006_alter_medicationreminder_frequency_per_day'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='medicationreminder',
            name='medication_taken',
        ),
        migrations.AlterField(
            model_name='medicationreminder',
            name='day',
            field=models.DateField(auto_now=True),
        ),
        migrations.CreateModel(
            name='MedicationReminderRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('remind_time', models.TimeField()),
                ('taken', models.BooleanField(default=False)),
                ('reminder', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reminder_records', to='reminders.medicationreminder')),
            ],
        ),
    ]