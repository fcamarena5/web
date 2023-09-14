from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from .search import SelectQueryDB
from .communicate import send_message
from .video import generate_video, detect_fire_or_person


# Redirects to Login page if user is not authenticated or to Main page if authenticated.
def default(request):
    if request.user.is_anonymous:
        return redirect('uned:login')
    else:
        return redirect('uned:home')

# Returns an 'user' object if valid credentials and redirects to main page
# if wrong credentials then redirects to login page
def login_auth(request):
    if not request.user.is_anonymous:
        return redirect('uned:home')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        # Creates an 'user' object if valid credentials
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            context = {'user': request.user}
            return redirect('uned:home')
        else:
            context = {'wrong_credentials': True}
    else:
        context = {}
    return render(request, 'login.html', context)

# Closes the session and redirects to Login page.
@login_required(login_url='login')
def logout_auth(request):
    logout(request)
    return redirect('uned:login')

# - If passwords match, changes the user's password.
# - Returns a HttpResponse to Ajax in change_password.js indicating:
#    > 1 if password was changed successfully. 
#    > 0 if passwords do not match.
# - As CSRF token is not passed by Ajax, this function is exempted for this requirement.
@csrf_exempt
@login_required(login_url='login')
def change_password(request):
    try:
        if request.method == 'POST':
            username = request.user.username
            new_password1 = request.POST.get('new_password_1')
            new_password2 = request.POST.get('new_password_2')
            old_password = request.POST.get('old_password')
            right_old_password = request.user.check_password(old_password)
            if new_password1 == new_password2 and new_password1 is not None and right_old_password:
                user_object = User.objects.get(username=username)
                user_object.set_password(new_password1)
                user_object.save()
                password_changed = 1
            else:
                password_changed = 0
            return HttpResponse(password_changed)
    except Exception as e:
        return HttpResponse(e)
    
@login_required(login_url='uned:login')
def home(request):
    mac = request.POST.get('mac', '') if 'mac' in request.POST else None
    if 'button_actuators' in request.POST:
        angle_servo1 = request.POST.get('servo1')
        angle_servo2 = request.POST.get('servo2')
        send_message(mac, angle_servo1, angle_servo2)

    data = SelectQueryDB(request).get_data()
    chart_temperature, chart_light = SelectQueryDB(request).get_charts(mac)
    context = {
        'title': 'Home',
        'devices': data,
        'selected_device': mac,
        'temperature_chart_json': chart_temperature,
        'light_chart_json': chart_light
    }
    return render(request, 'home.html', context)

@login_required(login_url='uned:login')
def thermal(request, mac):
    data = SelectQueryDB(request).get_data()
    thermal_data = SelectQueryDB(request).get_thermal_data(mac)
    generate_video(thermal_data)
    list_fire, list_person = detect_fire_or_person(thermal_data)
    context = {
        'title': 'Thermal' + mac,
        'thermal_data': thermal_data,
        'devices': data,
        'mac': mac,
        'detected_fire': list_fire,
        'detected_person': list_person
    }
    return render(request, 'thermal.html', context)

@login_required(login_url='uned:login')
def actions(request):
    if 'button_graph' in request.POST:
        redirect('uned:home')
    else:
        home(request)
