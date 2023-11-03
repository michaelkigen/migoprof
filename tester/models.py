from django.db import models

# Create your models here.
class Test(models.model):
    quiz = models.CharField(max_length=300)
    points = models.IntegerField()