import cv2
import os
import csv

# -----------------------------
# Student Details
# -----------------------------

student_id = input("Enter Student ID: ").strip()
name = input("Enter Student Name: ").strip()
department = input("Enter Department: ").strip()
year = input("Enter Year: ").strip()

# -----------------------------
# Create Dataset Folder
# -----------------------------

dataset_path = "dataset"
person_path = os.path.join(dataset_path, name)

# Check if student already exists
if os.path.exists(person_path):
    print("\nStudent already registered!")
    exit()

os.makedirs(person_path)

print("\nSaving images to:", person_path)

# -----------------------------
# Update students.csv
# -----------------------------

csv_file = "students.csv"

# Create file if it doesn't exist
if not os.path.exists(csv_file):
    with open(csv_file, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["ID", "Name", "Department", "Year"])

# Check duplicate ID
duplicate = False

with open(csv_file, "r") as file:
    reader = csv.DictReader(file)

    for row in reader:
        if row["ID"] == student_id:
            duplicate = True
            break

if duplicate:
    print("\nStudent ID already exists!")
    exit()

# Add student details
with open(csv_file, "a", newline="") as file:
    writer = csv.writer(file)

    writer.writerow([
        student_id,
        name,
        department,
        year
    ])

print("Student details saved successfully!")

# -----------------------------
# Open Camera
# -----------------------------

cap = cv2.VideoCapture(0)

count = 0
max_images = 50

while True:

    ret, frame = cap.read()

    if not ret:
        print("Camera Error!")
        break

    cv2.imshow("Face Registration", frame)

    img_path = os.path.join(person_path, f"{count}.jpg")

    cv2.imwrite(img_path, frame)

    print(f"Image {count + 1} Saved")

    count += 1

    if count >= max_images:
        break

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

print("\n--------------------------------")
print("Student Registered Successfully!")
print(f"ID         : {student_id}")
print(f"Name       : {name}")
print(f"Department : {department}")
print(f"Year       : {year}")
print("--------------------------------")