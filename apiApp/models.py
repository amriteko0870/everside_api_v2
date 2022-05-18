from django.db import models

# Create your models here.

class everside_nps(models.Model):
    review_id = models.CharField(max_length=100)
    review = models.CharField(max_length=100)
    label = models.CharField(max_length=100)
    polarity_score = models.CharField(max_length=100)
    nps_score = models.CharField(max_length=100)
    nps_label = models.CharField(max_length=100)
    date = models.CharField(max_length=100)
    clinic = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    timestamp = models.BigIntegerField()
    
class everside_clinic(models.Model):
    clinic = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
