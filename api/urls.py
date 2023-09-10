from django.urls import path
from .views import create_user, login, DeviceApiView, DataApiView, DataThermalApiView

urlpatterns = [
    path('register/', create_user, name='create_user'),
    path('login/', login, name='login'),
    path('add_device/', DeviceApiView.as_view()),
    path('add_data/', DataApiView.as_view()),
    path('thermal/', DataThermalApiView.as_view())
]