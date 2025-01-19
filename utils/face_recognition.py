import math
from random import randint
import time

import face_recognition
import numpy as np
from utils.encodings import get_face_encodings
from utils.attendance import AttendanceTracker
from utils.face_list import known_faces_list

unique_names = []
face_names = []
tolerance = 0.5


# unknown_faces_list, known_face_encodings, known_face_names, known_face_melli, persons = load_encodings()

def face_confidence(face_distance):
    range = (1.0 - tolerance)
    linear_val = (1.0 - face_distance) / (range * 2.0)
    if face_distance > tolerance:
        return str(round(linear_val * 100, 2)) + "%"
    else:
        value = (linear_val + ((1.0- linear_val) * math.pow((linear_val - 0.5) * 2, 0.2))) * 100
        return str(round(value, 2)) + "%"
        
def process_face_recognition(frame, face_encodings, face_locations):
    global tolerance
    global unique_names, face_names
    global known_faces_list
    global unknown_faces_list, known_face_encodings, known_face_names, known_face_melli, persons

    unknown_faces_list, known_face_encodings, known_face_names, known_face_melli, persons = get_face_encodings()

    for face_encoding, (top, right, bottom, left) in zip(face_encodings, face_locations):
        name = "Unknown"
        confidence = 'Unknown'
        melli = ''

        top -= int((bottom - top) * 0.34)
        bottom += int((bottom - top) * 0.09)
        left -= int((right - left) * 0.09)
        right += int((right - left) * 0.09)
        face_image = frame[top:bottom, left:right]

        # Show face landmarks for unknown faces
        face_landmarks_list = face_recognition.face_landmarks(face_image)
        required_features = {"chin", "left_eyebrow", "right_eyebrow", "nose_bridge", "nose_tip", "left_eye", "right_eye", "top_lip", "bottom_lip"}

        # Check if all required features are present
        if face_landmarks_list and all(feature in face_landmarks_list[0] for feature in required_features):

            if known_face_encodings:
                # Proceed with operations that depend on known_face_encodings
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=tolerance)
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)

                if matches[best_match_index]:
                    name = known_face_names[best_match_index]
                    melli = known_face_melli[best_match_index]
                    confidence = face_confidence(face_distances[best_match_index])

            face_names.append(f"{name} ({confidence})")

            if name != "Unknown":
                tracker = AttendanceTracker()
                if name not in unique_names:
                    unique_names.append(name)
                    known_faces_list.append((melli, name, face_image, confidence, [], face_encoding, int(time.time()), int(time.time())))
                    tracker.add_attendance(melli, face_image)
                    # add_known_face(melli, name, face_image)
                    
                else:
                    tracker.update_attendance(melli)

                for i, (saved_melli, saved_name, saved_image, saved_confidence, landmarks_list, _, insertAt, updateAt) in enumerate(known_faces_list):
                    if saved_melli == melli:
                        try:
                            if float(confidence.rstrip('%')) > float(saved_confidence.rstrip('%')):
                                known_faces_list[i] = (saved_melli, name, face_image, confidence, [], face_encoding, insertAt, int(time.time()))
                        except ValueError:
                            pass
                        break

            else:
                name = f"Unknown{randint(0, 1000)}"
                if unknown_faces_list:
                    unknown_face_encodings = [unknown_face_encoding for _, _, _, _, unknown_face_encoding, _, _ in unknown_faces_list]
                    matches = face_recognition.compare_faces(unknown_face_encodings, face_encoding, tolerance=tolerance)
                    face_distances = face_recognition.face_distance(unknown_face_encodings, face_encoding)
                    best_match_index = np.argmin(face_distances)
                    if matches[best_match_index]:
                        name = unknown_faces_list[best_match_index][0]
                        insertAt = unknown_faces_list[best_match_index][5]
                        confidence = face_confidence(face_distances[best_match_index])
                        unknown_faces_list[best_match_index] = (name, face_image, confidence, face_landmarks_list, face_encoding, insertAt, int(time.time()))
                        return
                unknown_faces_list.append((name, face_image, confidence, face_landmarks_list, face_encoding, int(time.time()), int(time.time())))

    return face_names