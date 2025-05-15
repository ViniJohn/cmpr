from django.db import models

# Create your models here.
# models.py
from django.db import models

class Item(models.Model):
    name = models.CharField(max_length=100)
    itemflag = models.BooleanField(default=False)
    reportnumber = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Vendor(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='vendors')
    vendorname = models.CharField(max_length=100)
    value = models.IntegerField()
    vendorflag = models.BooleanField(default=False)

    def __str__(self):
        return self.vendorname
