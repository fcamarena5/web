from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from .serializers import UserSerializer, DeviceSerializer, DataSerializer, DataThermalSerializer
from uned.communicate import check_updated_ip
from datetime import datetime


@api_view(['POST'])
def create_user(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            password = make_password(request.data['password'])
            serializer.save(password=password)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login(request):
    if request.method == 'POST':
        username = request.data['username']
        password = request.data['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
class DeviceApiView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        user_data = User.objects.filter(username=request.data.get('username')).values('id').first()
        if user_data:
            user_id = user_data['id']
            data = {
                'name': request.data.get('name'),
                'mac': request.data.get('mac'),
                'ip': request.data.get('ip'),
                'user': user_id,
                'last_connection': datetime.today()
            }
            serializer = DeviceSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
   
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class DataApiView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        data = {
            'mac': str(request.data.get('mac')),
            'ip': str(request.data.get('ip')),
            'time': datetime.today(),
            'angle_servo1': int(request.data.get('angle_servo1')),
            'angle_servo2': int(request.data.get('angle_servo2')),
            'temperature': float(request.data.get('temperature')),
            'light': float(request.data.get('light'))
        }
        check_updated_ip(request.data.get('mac'), request.data.get('ip'))
        serializer = DataSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class DataThermalApiView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        data = {
            'mac': str(request.data.get('mac')),
            'ip': str(request.data.get('ip')),
            'time': datetime.today(),
            'pixels': str(request.data.get('pixels'))
        }
        check_updated_ip(request.data.get('mac'), request.data.get('ip'))
        serializer = DataThermalSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
