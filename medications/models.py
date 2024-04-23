from django.db import models

# Create your models here.
class Medication(models.Model):

    PHARMACEUTICAL_FORM = [
        ('tablet', 'Tablet'),
        ('capsule', 'Capsule'),
        ('solution', 'Solution'),
        ('liquid', 'Liquid'),
        ('injectable', 'Injectable'),
    ]
    name = models.CharField(max_length=250, verbose_name='Medication name')
    pharmaceutical_form = models.CharField(max_length=20, choices=PHARMACEUTICAL_FORM, verbose_name='Pharmaceutical form')
    medical_prescripion_id = models.IntegerField(null=True, blank=True, unique=True, verbose_name='Medical prescription id')