from flask import Flask, request,jsonify
#from werkzeug.utils import secure_filename
from flask_cors import CORS
import os
import csv
from datetime import datetime
import face_recognition


app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET'])
def hello():
    str='HELLO FROM FLASK'
    return jsonify(str)


known_faces_directory = "images"
csv_file = "attendance.csv"

def load_known_faces(directory):
    known_faces = []
    known_names = []

    for filename in os.listdir(directory):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            image_path = os.path.join(directory, filename)
            face_image = face_recognition.load_image_file(image_path)
            face_encoding = face_recognition.face_encodings(face_image)[0]
            known_faces.append(face_encoding)
            known_names.append(os.path.splitext(filename)[0])  # Use file name as the person's name

    return known_faces, known_names

known_faces, known_names = load_known_faces(known_faces_directory)

def mark_attendance(name):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(csv_file, mode='a', newline='') as file:
        writer = csv.writer(file)

        # Write the header if the file is empty
        if os.path.getsize(csv_file) == 0:
            writer.writerow(['Timestamp', 'Name'])

        # Write attendance data if not detected already on the same day
        if not is_already_detected_today(name):
            writer.writerow([timestamp, name])
            print("Attendance marked for:", name)
        else:
            print("Already attendance marked today")


def is_already_detected_today(name):
    today = datetime.now().strftime("%Y-%m-%d")
    try:
        with open(csv_file, mode='r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip the header
            for row in reader:
                if row:  # Check if the row is not empty
                    timestamp, detected_name = row
                    date = timestamp.split()[0]
                    if date == today and detected_name == name:
                        return True
    except FileNotFoundError:
        return False  # Return False if the file does not exist
    except StopIteration:
        return False  # Return False if the file is empty after skipping header
    return False


def recognize_face(image):
    
    # Load the image
    unknown_image = face_recognition.load_image_file(image)
    unknown_face_encodings = face_recognition.face_encodings(unknown_image)

    # Loop through each face in the image
    for unknown_face_encoding in unknown_face_encodings:
        # Compare the face with known faces
        matches = face_recognition.compare_faces(known_faces, unknown_face_encoding)

        if True in matches:
            first_match_index = matches.index(True)
            name = known_names[first_match_index]
            mark_attendance(name)
            return name

    return "Unknown"

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'image' not in request.files:
        return 'No file part'
    print("upload button pressed")
    file = request.files['image']
    
    if file.filename == '':
        return 'No selected file'
    
    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        detected_name = recognize_face(file_path)
        return 'Attendance marked for: ' + detected_name if detected_name != "Unknown" else 'Face not recognized'



if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
