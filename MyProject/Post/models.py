from turtle import title
from django.db import models

CATEGORY_CHOICES = (
    ('Dj','Django'),
    ('R',"Ruby")
)
# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=100)
    custom_id = models.IntegerField()
    category  = models.CharField(max_length=3, choices=CATEGORY_CHOICES)
    publish_date = models.DateTimeField(auto_now_add=True)
    last_updated  = models.DateField(auto_now=True)



