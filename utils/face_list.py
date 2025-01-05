from utils.encodings import load_encodings

unknown_faces_list, known_face_encodings, known_face_names, known_face_melli,_ = load_encodings()
known_faces_list = []


def get_unknown_faces_list():
    global unknown_faces_list
    unknown_faces_list.sort(key=lambda x: x[6], reverse=True)
    return unknown_faces_list

def get_known_faces_list():
    global known_faces_list
    known_faces_list.sort(key=lambda x: x[6], reverse=True)
    return known_faces_list