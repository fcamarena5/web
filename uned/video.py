#import cv2
import numpy as np


def parse_pixels(pixels_string):
    pixels_list = [float(x) for x in pixels_string.split(',')]
    pixels_matrix = np.array(pixels_list).reshape(8, 8)
    return pixels_matrix.tolist()

def generate_video(thermal_data):
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('thermal_video.avi', fourcc, 20.0, (8, 8), isColor=False)
    for data in thermal_data:
        pixels_matrix = parse_pixels(data.pixels)
        # Normalize the values
        pixels_matrix = (pixels_matrix - np.min(pixels_matrix)) / (np.max(pixels_matrix) - np.min(pixels_matrix))
        pixels_matrix = (pixels_matrix * 255).astype(np.uint8)
        # Write every pixel in the vudeo
        out.write(pixels_matrix)
    out.release()


