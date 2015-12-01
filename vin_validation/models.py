from django.db import models

# Create your models here.
class Vehicle(models.Model):
    VIN = models.CharField(max_length=17, default="1FAFP40634F172825")
    Make = models.CharField(max_length=40)
    Modal = models.CharField(max_length=50)
    Year = models.CharField(max_length=4)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        pass