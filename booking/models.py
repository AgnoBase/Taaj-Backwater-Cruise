from django.db import models
from .constants import PaymentStatus
from django.utils.translation import gettext_lazy as _

# Create your models here.


class Plans(models.Model):

    name = models.CharField(max_length=50) 
    description=models.TextField()
    Duration1=models.IntegerField()
    price1=models.IntegerField()
    Duration2=models.IntegerField()
    price2=models.IntegerField()
    image = models.ImageField(upload_to='plan_img')
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}"
    

class Booking(models.Model):

    plan = models.ForeignKey(Plans,on_delete=models.CASCADE)
    fname = models.CharField(max_length=20)
    mname = models.CharField(max_length=10,null=True,blank=True)
    lname = models.CharField(max_length=20)
    email = models.EmailField(max_length=100)
    cnum = models.IntegerField()
    arrivedate = models.DateField()
    adults = models.IntegerField(null=True)
    child = models.IntegerField(blank=True)
    time = models.TimeField()
    date = models.DateTimeField(auto_now=True)
    ispaid= models.BooleanField(default=False) 
    amount = models.FloatField(_("Amount"), null=False, blank=False)
    status = models.CharField(
        _("Payment Status"),
        default=PaymentStatus.PENDING,
        max_length=254,
        blank=False,
        null=False,
    )
    provider_order_id = models.CharField(
        _("Order ID"), max_length=40, null=False, blank=False
    )
    payment_id = models.CharField(
        _("Payment ID"), max_length=36, null=False, blank=False
    )
    signature_id = models.CharField(
        _("Signature ID"), max_length=128, null=False, blank=False
    )

    def __str__(self):
        return f"{self.fname}{self.mname}{self.lname} booking on arrive date {self.arrivedate}"




