# Generated by Django 5.0.4 on 2024-09-08 01:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medications', '0004_remove_medication_medical_prescripion_id'),
        ('reminders', '0010_alter_amountreminder_medication'),
    ]

    operations = [
        migrations.AlterField(
            model_name='amountreminder',
            name='medication',
            field=models.OneToOneField(blank=True, on_delete=django.db.models.deletion.DO_NOTHING, to='medications.medication'),
        ),
    ]