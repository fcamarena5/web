from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

    
class Device(models.Model):
    name = models.CharField(max_length=30, blank=True, null=True)
    mac = models.CharField(max_length=12, primary_key=True, blank=False, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    last_connection = models.DateTimeField(blank=True, null=True)
    ip = models.GenericIPAddressField(blank=True, null=True)

    def __str__(self):
        return self.mac

class Data(models.Model):
    code = models.AutoField(primary_key=True, blank=False, null=False, auto_created=True)
    mac = models.ForeignKey(Device, blank=False, null=False, on_delete=models.CASCADE)
    time = models.DateTimeField(blank=True, null=True)
    angle_servo1 = models.IntegerField(blank=True, null=True)
    angle_servo2 = models.IntegerField(blank=True, null=True)
    temperature = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    light = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)

    def __int__(self):
        return self.code
    
class DataThermal(models.Model):
    code = models.AutoField(primary_key=True, blank=False, null=False, auto_created=True)
    mac = models.ForeignKey(Device, blank=False, null=False, on_delete=models.CASCADE)
    time = models.DateTimeField(blank=True, null=True)
    pixels = models.CharField(max_length=1024, blank=True, null=True)

    def __int__(self):
        return self.code
    
