import cv2
import numpy as np
from datetime import datetime


def get_color(temperature):
    if temperature > 50 and temperature < 70:
        return (0, 153, 255)
    elif temperature >= 70:
        return (0, 0, 255)
    elif temperature > 30 and temperature <= 50:
        return (0, 255, 255)
    elif temperature > 20 and temperature <= 30:
        return (0, 200, 0)
    elif temperature > 10 and temperature <= 20:
        return (255, 255, 0)
    elif temperature <= 10:
        return (255, 255, 0)

def parse_pixels(pixels_string):
    pixels_list = pixels_string.split(",")
    pixels_list = pixels_list[:-1]
    pixels_list = [float(x) for x in pixels_list]
    return pixels_list

def generate_video(thermal_data):
    # Create a VideoWriter object to save the video
    fourcc = cv2.VideoWriter_fourcc(*'vp09')
    video_filename = 'media/videos/temperature_video.webm'
    video_writer = cv2.VideoWriter(video_filename, fourcc, 1, (8, 8))

    # Iterate through the temperature data and create the frames for the video
    i = 0
    for data in thermal_data:
        temperature_values = parse_pixels(data.pixels)
        temperature_values = [get_color(temperature) for temperature in temperature_values]
        frame = np.array(temperature_values).reshape(8, 8, 3).astype(np.uint8)
        video_writer.write(frame)
        i += 1
        if i == 60:
            break
    video_writer.release()
    return None

def filter_alerts(alerts):
    new_list = []
    for alert in alerts:
        if len(new_list) == 0:
            new_list.append(alert)
        else:
            hour = int(alert.split(":")[0][-2:])
            minute = int(alert.split(":")[1])
            hour_last_alert = int(new_list[-1].split(":")[0][-2:])
            minute_last_alert = int(new_list[-1].split(":")[1])
            current_event = datetime(2023, 9, 14, hour, minute)
            last_event = datetime(2023, 9, 14, hour_last_alert, minute_last_alert)
            difference_time = current_event - last_event
            if difference_time.total_seconds() > 300:
                new_list.append(alert)
    return new_list

def detect_fire_or_person(thermal_data):
    detected_fire = []
    detected_person = []
    frame = 0
    for data in thermal_data:
        temperature_values = parse_pixels(data.pixels)
        pixels_temp_person = [i for i in range(len(temperature_values)) if temperature_values[i] > 30 and temperature_values[i] < 50]
        pixels_temp_fire = [i for i in range(len(temperature_values)) if temperature_values[i] >= 50]
        temp_person = [temp for temp in temperature_values if temp > 30 and temp < 50]
        temp_fire = [temp for temp in temperature_values if temp >= 50]
        if len(pixels_temp_person) > 0:
            detected_fire.append('Person detected at ' + str(data.time) + ' with a temperature of ' + str(max(temp_person)) + 'C')
        if len(pixels_temp_fire) > 0:
            detected_fire.append('Fire detected at ' + str(data.time) + ' with a temperature of ' + str(max(temp_fire)) + 'C')
        frame += 1
        if frame == 60:
            break
    detected_fire = filter_alerts(detected_fire)
    detected_person = filter_alerts(detected_person)
    return detected_fire, detected_person
        



