import pandas as pd
import os


class Student:
    def __init__(self, name, net_id, score):
        self.name = name
        self.net_id = net_id
        self.score = score

    def serialize(self):
        return {
            "name": self.name,
            "net_id": self.net_id,
            "score": self.score
        }

def print_students(students):
    print([student.serialize() for student in students])

def create_students():
    students_file = open("students.txt", "r")
    line = students_file.readline()
    students = []
    while line:
        net_id = line.rstrip("\n").rstrip("\t")
        student = Student(name="", net_id=net_id, score=0)
        students.append(student)
        line = students_file.readline()
    students_file.close()
    return students

def calculate_scores(students, filename):
    xls = pd.ExcelFile(filename)
    df1 = pd.read_excel(xls, "Final Scores")
    for index, row in df1.iterrows():
        net_id = str(row[1]).lower()
        for student in students:
            if net_id == student.net_id:
                score = row[2]
                student.score += score
    return students

def get_kahoot_leaderboard():
    students = create_students()
    for filename in os.listdir("."):
        if filename.endswith("xlsx") and not filename.startswith("~$"):
            students = calculate_scores(students, filename)
    leaderboard = sorted(students, key=lambda student: -student.score)
    return [student.serialize() for student in leaderboard]

def get_attendance():
    attendance = {}
    lecture_num = 0
    for filename in os.listdir("."):
        if filename.endswith("xlsx") and not filename.startswith("~$"):
            lecture_num += 1
            xls = pd.ExcelFile(filename)
            df1 = pd.read_excel(xls, "Final Scores")
            for index, row in df1.iterrows():
                net_id = str(row[1]).lower()
                if not net_id in attendance:
                    attendance[net_id] = int((1 / lecture_num) * 100)
                else:
                    attendance[net_id] = int(((attendance[net_id] + 1) / lecture_num) * 100)
    return attendance