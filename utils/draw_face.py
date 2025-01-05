import cv2
from PIL import Image, ImageTk
import tkinter as tk

def draw_faces(frame, face_locations, face_names):
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        center_x, center_y = (left + right) // 2, (top + bottom) // 2
        radius = int(max(right - left, bottom - top) * 1.2) // 2

        color = (0, 255, 0) if "Unknown" not in name else (0, 0, 255)
        cv2.circle(frame, (center_x, center_y), radius, color, 1)

        # font = cv2.FONT_HERSHEY_SIMPLEX
        # cv2.putText(frame, name, (left + 6, top - 6), font, 0.5, (255, 255, 255), 1)

    return frame