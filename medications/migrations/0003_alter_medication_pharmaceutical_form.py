# Generated by Django 5.0.4 on 2024-07-07 01:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medications', '0002_remove_medication_patient_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medication',
            name='pharmaceutical_form',
            field=models.CharField(choices=[('tablet', 'Tablet'), ('capsule', 'Capsule'), ('solution', 'Solution'), ('liquid', 'Liquid'), ('drops', 'Drops'), ('injectable', 'Injectable')], max_length=20, verbose_name='Pharmaceutical form'),
        ),
    ]
