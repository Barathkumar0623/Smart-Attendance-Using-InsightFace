from flask import Flask, render_template
import csv
import json
from datetime import datetime

app = Flask(__name__)

# -----------------------------
# Total Students
# -----------------------------
def total_students():
    try:
        with open("students.csv", "r") as file:
            return max(sum(1 for _ in file) - 1, 0)
    except Exception:
        return 0


# -----------------------------
# Total Attendance Records
# -----------------------------
def total_attendance():
    try:
        with open("attendance.csv", "r") as file:
            return max(sum(1 for _ in file) - 1, 0)
    except Exception:
        return 0


# -----------------------------
# Today's Attendance
# -----------------------------
def today_attendance():

    try:

        today = datetime.now().strftime("%d-%m-%Y")

        count = 0

        with open("attendance.csv", "r") as file:

            reader = csv.DictReader(file)

            for row in reader:

                if row["Date"] == today:
                    count += 1

        return count

    except Exception:

        return 0


# -----------------------------
# Latest Emotion
# -----------------------------
def latest_emotion():

    try:

        emotion = "N/A"

        with open("attendance.csv", "r") as file:

            reader = csv.DictReader(file)

            for row in reader:
                emotion = row.get("Expression", "N/A")

        return emotion

    except Exception:

        return "N/A"


# -----------------------------
# Average Recognition
# -----------------------------
def average_recognition():

    try:

        total = 0
        count = 0

        with open("attendance.csv", "r") as file:

            reader = csv.DictReader(file)

            for row in reader:

                value = row.get("Recognition", "0")
                value = value.replace("%", "")

                total += float(value)
                count += 1

        if count == 0:
            return 0

        return round(total / count, 2)

    except Exception:

        return 0
    
# -----------------------------
# Attendance Trend Chart
# -----------------------------
def attendance_chart():

    data = {}

    try:

        with open("attendance.csv", "r") as file:

            reader = csv.DictReader(file)

            for row in reader:

                date = row["Date"]

                data[date] = data.get(date, 0) + 1

    except Exception:
        pass

    return {
        "labels": list(data.keys()),
        "values": list(data.values())
    }


# -----------------------------
# Emotion Distribution Chart
# -----------------------------
def emotion_chart():

    emotions = {}

    try:

        with open("attendance.csv", "r") as file:

            reader = csv.DictReader(file)

            for row in reader:

                emotion = row.get("Expression", "Unknown")

                emotions[emotion] = emotions.get(emotion, 0) + 1

    except Exception:
        pass

    return {
        "labels": list(emotions.keys()),
        "values": list(emotions.values())
    }


# -----------------------------
# Home Dashboard
# -----------------------------
@app.route("/")
def home():

    recent = []

    try:

        with open("attendance.csv", "r") as file:

            reader = list(csv.DictReader(file))

            recent = reader[-5:]

            recent.reverse()

    except:
        pass

    return render_template(
    "index.html",
    students=total_students(),
    attendance=total_attendance(),
    today=today_attendance(),
    recognition=average_recognition(),
    emotion=latest_emotion(),
    recent=recent,
    attendance_chart=json.dumps(attendance_chart()),
    emotion_chart=json.dumps(emotion_chart())
    
)


# -----------------------------
# Students Page
# -----------------------------
@app.route("/students")
def students():

    students_list = []

    try:

        with open("students.csv", "r") as file:

            reader = csv.DictReader(file)

            for row in reader:
                students_list.append(row)

    except Exception as e:

        print("Students Error:", e)

    return render_template(
        "students.html",
        students=students_list
    )


# -----------------------------
# Attendance Page
# -----------------------------
@app.route("/attendance")
def attendance():

    attendance_list = []

    try:

        with open("attendance.csv", "r") as file:

            reader = csv.DictReader(file)

            for row in reader:
                attendance_list.append(row)

    except Exception as e:

        print("Attendance Error:", e)

    return render_template(
        "attendance.html",
        attendance=attendance_list
    )


# -----------------------------
# Run Flask App
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)