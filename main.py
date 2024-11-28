import cv2
import time
import json
import pymysql
import os
import numpy as np

# Load the trained face recognizer model and label dictionary
model_path = 'face_model.yml'
label_dict_path = 'label_dict.json'
registration_file = 'user_registration.txt'  # File to store registration number

try:
    face_recognizer = cv2.face.LBPHFaceRecognizer_create()
    face_recognizer.read(model_path)
    
    with open(label_dict_path, 'r') as f:
        label_dict = json.load(f)
    
    # Reverse the label dictionary to map numbers back to names
    label_dict_reversed = {v: k for k, v in label_dict.items()}

except Exception as e:
    print(f"Error loading model or label dictionary: {e}")
    exit()

# Initialize face detector
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Start video capture
cam = cv2.VideoCapture(1)

print("Starting face recognition for 15 seconds...")
start_time = time.time()
lowest_confidence = float('inf')  # Initialize with a very high value
lowest_confidence_name = "Unknown"

while time.time() - start_time < 15:  # Scan for 15 seconds
    ret, frame = cam.read()
    if not ret:
        print("Failed to access camera. Exiting...")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    for (x, y, w, h) in faces:
        face_img = gray[y:y + h, x:x + w]
        face_img_resized = cv2.resize(face_img, (400, 400))  # Match training size
        
        # Predict the label of the face
        label, confidence = face_recognizer.predict(face_img_resized)
        
        # Map the label back to the name
        name = label_dict_reversed.get(label, "Unknown")
        
        # Display the label and confidence on the frame
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        cv2.putText(frame, f"{name} ({confidence:.1f})", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)
        
        if confidence < lowest_confidence:
            lowest_confidence = confidence
            lowest_confidence_name = label_dict_reversed.get(label, "Unknown")
            
    cv2.imshow('Face Recognition', frame)

    # Exit on pressing 'Esc'
    if cv2.waitKey(1) == 27:
        break

# Release resources
cam.release()
cv2.destroyAllWindows()

if lowest_confidence_name != "Unknown":
    print(f"Best match: {lowest_confidence_name} with confidence {lowest_confidence:.2f}")
    
    # Ask the user if the recognized person is them
    is_user = input(f"Is this you, {lowest_confidence_name}? (yes/no): ").strip().lower()
    
    if is_user == "yes":
        # Check if the file exists and create it or write to it
        if os.path.exists(registration_file):
            with open(registration_file, 'a') as file:
                file.write(f"{lowest_confidence_name}: Present\n")
                print(f"Registration number {lowest_confidence_name} saved.")
        else:
            with open(registration_file, 'w') as file:
                file.write(f"{lowest_confidence_name}: Present\n")
                print(f"Registration number Marked for {lowest_confidence_name}.")
    else:
        print("It's not you. Exiting...")
else:
    print("No recognized faces.")



# Establish MySQL connection using pymysql
conn = pymysql.connect(
    host="localhost",
    user="root",
    password="auto1976bot",
    database="attendance_db"
)
cursor = conn.cursor()

# Path to the file containing attendance data
file_path = 'user_registration.txt'

# Check if the file exists
if os.path.exists(file_path):
    # Read the file content
    with open(file_path, 'r') as file:
        attendance_data = file.read()

    # Split the data by lines and process each line
    lines = attendance_data.strip().split('\n')

    for line in lines:
        registration_number, attendance_status = line.split(': ')
        
        # SQL query to update attendance
        sql = "UPDATE attendance SET attendance_status = %s WHERE registration_number = %s"
        cursor.execute(sql, (attendance_status, registration_number))
    
# Commit the changes to the database
    conn.commit()
    print("Attendance updated successfully.")
else:
    print(f"The file {file_path} does not exist.")

# Close the connection
cursor.close()
conn.close()