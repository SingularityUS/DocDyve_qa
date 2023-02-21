from django.db import models

class Document(models.Model):
    file = models.FileField(upload_to='documents/')

class Question(models.Model):
    text = models.CharField(max_length=255)
