from django.db import models


# Create your models here.

class ulasan(models.Model):
    nama = models.CharField(max_length=100)
