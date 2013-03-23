from django.db import models

# Create your models here.

class MirrorObject(models.Model):
    domain = models.CharField(max_length=20)
    code = models.CharField(max_length=10,unique=True)
    login = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    game_id = models.IntegerField()
