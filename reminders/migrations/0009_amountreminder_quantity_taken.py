# Generated by Django 5.0.4 on 2024-08-23 01:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reminders', '0008_alter_medicationreminder_day'),
    ]

    operations = [
        migrations.AddField(
            model_name='amountreminder',
            name='quantity_taken',
            field=models.IntegerField(default=1),
        ),
    ]