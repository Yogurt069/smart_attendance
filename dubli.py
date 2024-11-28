import cv2
import os
import json
import numpy as np

# Step 1: Create directory for saving face images
output_dir = 'faces'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Step 2: Initialize camera and face detector
cam = cv2.VideoCapture(1)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

name = input("Enter your REGISTRATION NO.: ").strip()
fname = input("Enter your Full Name: ")
# Ensure a valid name is provided
if not name:
    print("Name cannot be empty. Exiting...")
    cam.release()
    cv2.destroyAllWindows()
    exit()

count = 0
print("Starting face capture. Press 'Esc' to stop.")

while True:
    ret, frame = cam.read()
    if not ret:
        print("Failed to access camera. Exiting...")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    for (x, y, w, h) in faces:
        count += 1
        face_img = gray[y:y + h, x:x + w]
        img_path = os.path.join(output_dir, f"{name}_{count}.jpg")
        cv2.imwrite(img_path, face_img)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

    cv2.imshow('Capturing Faces', frame)

    # Stop capturing on 'Esc' key or after 20 samples
    if cv2.waitKey(1) == 27 or count >= 20:
        print("Face capture complete.")
        break

# Release camera and close OpenCV windows
cam.release()
cv2.destroyAllWindows()

# Step 3: Train the LBPH face recognizer
print("Training the face recognizer...")

# Initialize the face recognizer
face_recognizer = cv2.face.LBPHFaceRecognizer_create()

faces = []
labels = []
label_dict = {}

for i, filename in enumerate(os.listdir(output_dir)):
    path = os.path.join(output_dir, filename)
    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        print(f"Failed to load image: {path}")
        continue

    # Normalize image size for consistent training
    img = cv2.resize(img, (400, 400))
    faces.append(img)

    # Extract the label from the filename
    label = filename.split('_')[0]
    if label not in label_dict:
        label_dict[label] = len(label_dict)
    labels.append(label_dict[label])

if len(faces) == 0 or len(labels) == 0:
    print("No valid data for training. Exiting...")
    exit()

faces = np.array(faces)
labels = np.array(labels)

# Train the recognizer and save the model
face_recognizer.train(faces, labels)
model_path = 'face_model.yml'
face_recognizer.write(model_path)

# Save label mapping to a JSON file
label_dict_path = 'label_dict.json'
with open(label_dict_path, 'w') as f:
    json.dump(label_dict, f)

print(f"Training complete. Model saved to '{model_path}' and labels to '{label_dict_path}'.")
