# Generated by Django 5.0.4 on 2024-09-07 22:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('medications', '0003_alter_medication_pharmaceutical_form'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='medication',
            name='medical_prescripion_id',
        ),
    ]
