# Generated by Django 5.0.4 on 2024-04-23 23:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medications', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='medication',
            name='patient_id',
        ),
        migrations.AddField(
            model_name='medication',
            name='medical_prescripion_id',
            field=models.IntegerField(blank=True, null=True, unique=True, verbose_name='Medical prescription id'),
        ),
    ]
