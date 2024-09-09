from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE, PROTECT
from django.db.models.fields import CharField


# Create your models here.

class Type(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return f'''{self.name}'''


class Setting(models.Model):
    pLen = models.DecimalField(decimal_places=1, max_digits=8)
    pLenSeconds = models.BooleanField()
    interval = models.DecimalField(decimal_places=1, max_digits=8)
    intervalSeconds = models.BooleanField()
    count = models.IntegerField()
    bulb = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True) 
    again = models.BooleanField(default=False)

    def __str__(self):
        if(self.pLenSeconds):   len = self.pLen
        else:   len = f"1/{self.pLen}"

        if(self.intervalSeconds):   inter = self.interval
        else:   inter = f"1/{self.interval}"

        return f'''{len}-{inter}-{self.count}-{self.bulb}'''
    
class Run(models.Model):
    top = models.IntegerField()
    settings = models.ForeignKey(Setting, on_delete=models.PROTECT)

class Cycle(models.Model):
    name = models.CharField(max_length = 32, default="")
    Type = models.ForeignKey(Type, on_delete=models.PROTECT)
    settings = models.OneToOneField(Setting, on_delete=models.CASCADE)

    created = models.DateTimeField(auto_now_add=True) 
    updated = models.DateTimeField(auto_now=True)

    save = models.BooleanField(default=False) #If true it will save it in a list, else it just goes in history
    
    def __str__(self):
        return f'''{self.name}'''


