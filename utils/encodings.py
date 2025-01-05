import os
import pickle
import sqlite3

# List to store the encodings of the unknown faces
unknown_faces_list = []
# List to store the encodings of the known faces
known_face_encodings = []
# List to store the names of the known faces
known_face_names = []
# List to store the national IDs of the known faces
known_face_melli = []
# List to store the details of the known faces
persons = []
# The tolerance for face recognition
tolerance = 0.4


# Create a connection to the SQLite database
conn = sqlite3.connect('db/main.db')
# Create a cursor object to execute SQL statements
cursor = conn.cursor()
# Create the table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS encodings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_id INTEGER,
        face_encoding BLOB
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS persons (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        melli TEXT,
        first_name TEXT,
        last_name TEXT,
        mobile TEXT
    )
''')

# Close the database connection
conn.close()

def remove_face_from_list(name):
    global unknown_faces_list
    print(f"Remove image: {name}")
    for i, (saved_name, _, _, _, _, _, _) in enumerate(unknown_faces_list):
        if saved_name == name:
            unknown_faces_list.pop(i)
            break

def save_encoding(name, face_encoding, melli, first_name, last_name, mobile):
    global unknown_faces_list, known_face_encodings, known_face_names, persons

    # Convert the face encoding to a binary string
    face_encoding_bytes = pickle.dumps(face_encoding)

    conn = sqlite3.connect('db/main.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM encodings')
    # Insert the data into the table
    cursor.execute('''
        INSERT INTO persons (melli, first_name, last_name, mobile)
        VALUES (?, ?, ?, ?)
    ''', (melli, first_name, last_name, mobile))
    conn.commit()
    person_id = cursor.lastrowid
    print('Person Saved', person_id)

    cursor.execute('''
        INSERT INTO encodings (person_id, face_encoding)
        VALUES (?, ?)
    ''', (person_id, face_encoding_bytes))
    conn.commit()
    print('Encoding Saved')

    persons.append([melli, first_name, last_name, mobile])
    known_face_encodings.append(face_encoding)
    known_face_names.append(first_name + " " + last_name)
    known_face_melli.append(melli)

    remove_face_from_list(name)

    conn.close()
    return unknown_faces_list, known_face_encodings, known_face_names, known_face_melli, persons
    
def load_encodings():
    global unknown_faces_list, known_face_encodings, known_face_names, known_face_melli, persons
    
    persons = []
    known_face_encodings = []
    known_face_names = []

    conn = sqlite3.connect('db/main.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM encodings')
    encodings = cursor.fetchall()
    for encoding in encodings:
        person_id = encoding[1]
        face_encoding = pickle.loads(encoding[2])
        cursor.execute('SELECT * FROM persons WHERE id = ?', (person_id,))
        person = cursor.fetchone()
        melli = person[1]
        first_name = person[2]
        last_name = person[3]
        mobile = person[4]
        persons.append([melli, first_name, last_name, mobile])
        known_face_encodings.append(face_encoding)
        known_face_names.append(first_name + " " + last_name)
        known_face_melli.append(melli)

    conn.close()
    return unknown_faces_list, known_face_encodings, known_face_names, known_face_melli, persons

def get_face_encodings():
    global unknown_faces_list, known_face_encodings, known_face_names, known_face_melli, persons
    return unknown_faces_list, known_face_encodings, known_face_names, known_face_melli, persons

def update_person(melli, first_name, last_name, mobile):
    conn = sqlite3.connect('db/main.db')
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE persons SET melli = ?, first_name = ?, last_name = ?, mobile = ? WHERE melli = ?
    ''', (melli, first_name, last_name, mobile, melli))
    conn.commit()
    conn.close()

def delete_person(melli):
    conn = sqlite3.connect('db/main.db')
    cursor = conn.cursor()
    cursor.execute('''
        DELETE FROM encodings WHERE person_id IN (SELECT id FROM persons WHERE melli = ?)
    ''', (melli,))
    cursor.execute('''
        DELETE FROM persons WHERE melli = ?
    ''', (melli,))
    conn.commit()
    conn.close()

def get_persons():
    global persons
    return persons