# Generated by Django 5.0.4 on 2024-08-22 00:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reminders', '0005_amountreminder_low_stock_alter_amountreminder_amount_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medicationreminder',
            name='frequency_per_day',
            field=models.IntegerField(blank=True, default=1, null=True),
        ),
    ]
