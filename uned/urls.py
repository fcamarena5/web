from django.urls import path
from . import views

app_name = 'uned'
urlpatterns = [
    path('', views.default, name='default'),
    path('login/', views.login_auth, name='login'),
    path('logout/', views.logout_auth, name='logout'),
    path('change_password/', views.change_password, name='change_password'),
    path('home/', views.home, name='home'),
    path('thermal/<str:mac>/', views.thermal, name='thermal'),
    path('action/', views.actions, name='action')
]   