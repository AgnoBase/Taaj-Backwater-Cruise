from django.db import models

class Faq(models.Model):
    question = models.TextField()
    answer = models.TextField()
    date = models.DateTimeField(auto_now=True)

# Create your models here.
