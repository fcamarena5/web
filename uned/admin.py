from django.contrib import admin
from .models import Device, Data, DataThermal


admin.site.register(Device)
admin.site.register(Data)
admin.site.register(DataThermal)
