import csv
import os
from datetime import datetime

attendance_marked = set()


def mark_attendance(
    student,
    recognition_confidence,
    expression,
    expression_confidence
):

    if student is None:
        return "Unknown"

    student_id = student["ID"]

    if student_id in attendance_marked:
        return "Already Marked"

    attendance_marked.add(student_id)

    file_exists = os.path.exists("attendance.csv")

    with open("attendance.csv", "a", newline="") as file:

        writer = csv.writer(file)

        if not file_exists:

            writer.writerow([
                "ID",
                "Name",
                "Department",
                "Year",
                "Date",
                "Time",
                "RecognitionConfidence",
                "Expression",
                "ExpressionConfidence",
                "Status"
            ])

        now = datetime.now()

        writer.writerow([
            student["ID"],
            student["Name"],
            student["Department"],
            student["Year"],
            now.strftime("%d-%m-%Y"),
            now.strftime("%H:%M:%S"),
            f"{recognition_confidence:.2f}%",
            expression,
            f"{expression_confidence:.2f}%",
            "Present"
        ])

    return "Present"