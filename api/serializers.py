from rest_framework import serializers
from django.contrib.auth.models import User
from uned.models import Device, Data, DataThermal


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']

class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ['name', 'mac', 'ip', 'user', 'last_connection']

class DataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Data
        fields = ['code', 'mac', 'ip', 'time', 'angle_servo1', 'angle_servo2', 'temperature', 'light']

class DataThermalSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataThermal
        fields = ['code', 'mac', 'ip', 'time', 'pixels']

