from django.http import HttpResponse
from .models import Device
import requests


def send_message(mac, servo1, servo2):
    ip = Device.objects.filter(mac=mac).first().ip
    url = "http://{address}/move_servo?servo1={servo1}&servo2={servo2}".format(address=ip, servo1=str(servo1), servo2=str(servo2))
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return HttpResponse("Solicitud enviada con éxito al ESP32")
        else:
            return HttpResponse("Error al enviar la solicitud al ESP32")
    except requests.exceptions.RequestException as e:
        return HttpResponse(f"Error de conexión: {e}")
    
def check_updated_ip(mac, current_ip):
    ip = Device.objects.filter(mac=mac).first().ip
    if current_ip != ip:
        device = Device.objects.get(mac=mac)
        device.ip = current_ip
        device.save()