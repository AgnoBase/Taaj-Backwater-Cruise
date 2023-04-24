from django.db import models

# Create your models here.
class Plans(models.Model):
    name = models.CharField(max_length=50) 
    description=models.TextField()
    Duration1=models.IntegerField()
    price1=models.IntegerField()
    Duration2=models.IntegerField()
    price2=models.IntegerField()
    
    def __str__(self):
     return f"{self.name}"
    
class Booking(models.Model):
    plan = models.ForeignKey(Plans,on_delete=models.CASCADE)
    fname = models.CharField(max_length=20)
    mname = models.CharField(max_length=10)
    lname = models.CharField(max_length=20)
    email = models.EmailField(max_length=100)
    cnum = models.IntegerField()
    arrivedate = models.DateField()
    time = models.TimeField()

