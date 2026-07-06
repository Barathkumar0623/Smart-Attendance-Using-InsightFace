import os
import csv
import cv2
import numpy as np
from insightface.app import FaceAnalysis
from attendance import mark_attendance
from expression import detect_expression

print("Loading AI Model...")

# -----------------------------
# Load InsightFace Model
# -----------------------------
app = FaceAnalysis(name="buffalo_l")
app.prepare(ctx_id=-1)

print("Loading AI Model...")

# -----------------------------
# Load Student Database
# -----------------------------
student_database = {}

with open("students.csv", "r") as file:
    reader = csv.DictReader(file)

    for row in reader:
        student_database[row["Name"]] = {
            "ID": row["ID"],
            "Department": row["Department"],
            "Year": row["Year"]
        }

print("Student Database Loaded Successfully!")
print(student_database)
print()
# -----------------------------
# Load Dataset
# -----------------------------
dataset_path = "dataset"

known_faces = []
known_names = []

print("Generating Face Embeddings...\n")

for person in os.listdir(dataset_path):

    person_path = os.path.join(dataset_path, person)

    if not os.path.isdir(person_path):
        continue

    for image_name in os.listdir(person_path):

        image_path = os.path.join(person_path, image_name)

        image = cv2.imread(image_path)

        if image is None:
            continue

        faces = app.get(image)

        if len(faces) == 0:
            continue

        known_faces.append(faces[0].embedding)
        known_names.append(person)

print("--------------------------------")
print("Embeddings Ready!")
print(f"Total Images : {len(known_faces)}")
print(f"Registered Persons : {len(set(known_names))}")
print("--------------------------------")

# -----------------------------
# Start Webcam
# -----------------------------
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Could not open webcam!")
    exit()
while True:

    ret, frame = cap.read()

    if not ret:
        break

    faces = app.get(frame)

    for face in faces:

        embedding = face.embedding

        best_score = -1
        best_name = "Unknown"

        # -----------------------------
        # Face Matching
        # -----------------------------
        for i, known_embedding in enumerate(known_faces):

            score = np.dot(
                embedding,
                known_embedding
            ) / (
                np.linalg.norm(embedding) *
                np.linalg.norm(known_embedding)
            )

            if score > best_score:
                best_score = score
                best_name = known_names[i]

        # -----------------------------
        # Threshold
        # -----------------------------
        confidence = best_score * 100

        SIMILARITY_THRESHOLD = 0.45

        if best_score < SIMILARITY_THRESHOLD:
            best_name = "Unknown"

        x1, y1, x2, y2 = face.bbox.astype(int)

        face_img = frame[y1:y2, x1:x2]

        emotion, emotion_confidence = detect_expression(face_img)

        color = (0,255,0)

        if best_name == "Unknown":
            color = (0,0,255)

        cv2.rectangle(frame,(x1,y1),(x2,y2),color,2)

        # -----------------------------
        # Student Found
        # -----------------------------
        if best_name != "Unknown":

            student = student_database.get(best_name)

            if student is not None:

                student_info = student.copy()
                student_info["Name"] = best_name

                status = mark_attendance(
                    student_info,
                    confidence,
                    emotion,
                    emotion_confidence
                )

                cv2.putText(
                    frame,
                    f"Name : {best_name}",
                    (20,30),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0,255,0),
                    2
                )

                cv2.putText(
                    frame,
                    f"ID : {student_info['ID']}",
                    (20,60),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0,255,0),
                    2
                )

                cv2.putText(
                    frame,
                    f"Department : {student_info['Department']}",
                    (20,90),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0,255,0),
                    2
                )

                cv2.putText(
                    frame,
                    f"Year : {student_info['Year']}",
                    (20,120),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0,255,0),
                    2
                )

                cv2.putText(
                    frame,
                    f"Status : {status}",
                    (20,150),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0,255,0),
                    2
                )

                cv2.putText(
                    frame,
                    f"Recognition : {confidence:.2f}%",
                    (20,180),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0,255,0),
                    2
                )

                cv2.putText(
                    frame,
                    f"Expression : {emotion}",
                    (20,210),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0,255,0),
                    2
                )

                cv2.putText(
                    frame,
                    f"Expression Confidence : {emotion_confidence:.2f}%",
                    (20,240),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0,255,0),
                    2
                )

        else:

            cv2.putText(
                frame,
                "Unknown Person",
                (20,30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0,0,255),
                2
            )

        # -----------------------------
        # Name Above Face
        # -----------------------------
        cv2.putText(
            frame,
            best_name,
            (x1, y1 - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            color,
            2
        )

    cv2.imshow("AI Smart Attendance System", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()