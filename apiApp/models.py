from django.db import models

# Create your models here.

# class userData(models.Model):
#     username = models.CharField(max_length=100)
#     passowrd = models.CharField(max_length=200)

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
    member_id = models.CharField(max_length=100,default='')
    survey_date = models.CharField(max_length=100,default='')
    survey_month = models.CharField(max_length=100,default='')
    survey_year = models.CharField(max_length=100,default='')
    survey_number = models.CharField(max_length=100,default='')
    clinic_id = models.CharField(max_length=100,default='')
    clinic_street = models.CharField(max_length=100,default='')
    clinic_city = models.CharField(max_length=100,default='')
    clinic_state = models.CharField(max_length=100,default='')
    clinic_zip = models.CharField(max_length=100,default='')
    clinic_type = models.CharField(max_length=100,default='')
    provider_name = models.CharField(max_length=100,default='')
    provider_type = models.CharField(max_length=100,default='')
    provider_category = models.CharField(max_length=100,default='')
    client_naics = models.CharField(max_length=100,default='')
    client_id = models.CharField(max_length=100,default='')
    client_name = models.CharField(max_length=100,default='')
    parent_client_id = models.CharField(max_length=100,default='')
    parent_client_name = models.CharField(max_length=100,default='')
    question_type = models.CharField(max_length=100,default='')
    
class everside_clinic(models.Model):
    clinic = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)


 