import cv2
import numpy as np


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
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video_filename = 'media/videos/temperature_video.mp4'
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



