from .models import Device, Data, DataThermal
import plotly.graph_objects as go


class SelectQueryDB:

    def __init__(self, request):
        self.request = request
        self.username = request.user.id

    def get_devices(self):
        objects = Device.objects.order_by('mac').filter(user=self.username)
        return objects
    
    def get_data(self):
        devices = self.get_devices()
        data_lists = []
        for device in devices:
            data = Data.objects.filter(mac=device.mac).order_by('-time').first()
            data_lists.append((device, data))
        return data_lists
    
    def get_charts(self, selected_device):
        if selected_device is None:
            selected_device = self.get_devices().first()
        datas = Data.objects.filter(mac=selected_device).order_by('-time')
        time_values = [data.time for data in datas]
        temperature_values = [data.temperature for data in datas]
        light_values = [data.light for data in datas]
        temperature_chart = go.Figure(go.Scatter(x=time_values, y=temperature_values, mode='lines'))
        light_chart = go.Figure(go.Scatter(x=time_values, y=light_values, mode='lines'))
        temperature_chart_json = temperature_chart.to_json()
        light_chart_json = light_chart.to_json()
        return temperature_chart_json, light_chart_json
    
    def get_thermal_data(self, mac):
        pixels = DataThermal.objects.filter(mac=mac).order_by('time')
        return pixels
        