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

def normalize_net_id(value):
    if pd.isna(value):
        return None
    net_id = str(value).strip().lower()
    if "@" in net_id:
        net_id = net_id.split("@", 1)[0]
    if net_id.endswith(".0") and net_id[:-2].isdigit():
        net_id = net_id[:-2]
    net_id = net_id.replace(" ", "")
    if not net_id or net_id == "nan":
        return None
    return net_id

def create_students():
    students = []
    with open("students.txt", "r", encoding="utf-8") as students_file:
        line = students_file.readline()
        while line:
            net_id = line.rstrip("\n").rstrip("\t")
            normalized_net_id = normalize_net_id(net_id)
            if normalized_net_id is not None:
                student = Student(name="", net_id=normalized_net_id, score=0)
                students.append(student)
            line = students_file.readline()
    return students

def extract_score(row):
    # Prefer columns explicitly named like "...score..."
    for col in row.index:
        if "score" in str(col).lower():
            score = pd.to_numeric(row[col], errors="coerce")
            if not pd.isna(score):
                return int(score)

    # Fallback for older/unexpected exports: third column.
    score = pd.to_numeric(row.iloc[2], errors="coerce")
    if pd.isna(score):
        return None
    return int(score)

def load_final_scores(filename):
    # Kahoot exports often include a title row above the real header.
    # We detect the header row by looking for cells like "Player" and "Total score".
    preview = pd.read_excel(filename, sheet_name="Final Scores", header=None, nrows=10)
    header_row = 0
    for i in range(len(preview)):
        cells = [str(x).strip().lower() for x in preview.iloc[i].tolist()]
        has_player = any(c == "player" or c.startswith("player ") for c in cells)
        has_total_score = any("total score" in c for c in cells)
        if has_player and has_total_score:
            header_row = i
            break

    return pd.read_excel(filename, sheet_name="Final Scores", header=header_row)

def find_column(columns, candidates):
    lowered = {str(col).strip().lower(): col for col in columns}
    for candidate in candidates:
        for key, original in lowered.items():
            if candidate in key:
                return original
    return None

def calculate_scores(students, filename):
    students_by_net_id = {student.net_id: student for student in students}
    df1 = load_final_scores(filename)
    player_col = find_column(df1.columns, ["player"])
    score_col = find_column(df1.columns, ["total score", "score"])
    for _, row in df1.iterrows():
        matched_student = None
        if player_col is not None:
            candidate_net_id = normalize_net_id(row[player_col])
            if candidate_net_id in students_by_net_id:
                matched_student = students_by_net_id[candidate_net_id]
        if matched_student is None:
            for value in row.tolist():
                candidate_net_id = normalize_net_id(value)
                if candidate_net_id in students_by_net_id:
                    matched_student = students_by_net_id[candidate_net_id]
                    break
        if matched_student is None:
            continue
        if score_col is not None:
            score = pd.to_numeric(row[score_col], errors="coerce")
            if pd.isna(score):
                continue
            score = int(score)
        else:
            score = extract_score(row)
        if score is None:
            continue
        matched_student.score += score
    return students

def get_kahoot_leaderboard(week_id=None):
    students = create_students()
    for filename in os.listdir("."):
        if week_id:
            if filename.endswith("xlsx") and \
                ((int(filename[filename.index("lecture") + 7:filename.index(".xlsx")]) + 1) // 2 == week_id) and \
                not filename.startswith("~$"):
                    students = calculate_scores(students, filename)
        else:
            if filename.endswith("xlsx") and not filename.startswith("~$"):
                students = calculate_scores(students, filename)
    leaderboard = sorted(students, key=lambda student: -student.score)
    output = []
    for i in range(len(leaderboard)):
        student = leaderboard[i].serialize()
        student["rank"] = i + 1
        output.append(student)
    return output

def get_attendance():
    attendance = {}
    lecture_num = 0
    for filename in os.listdir("."):
        if filename.endswith("xlsx") and not filename.startswith("~$"):
            lecture_num += 1
            df1 = load_final_scores(filename)
            player_col = find_column(df1.columns, ["player"])
            for _, row in df1.iterrows():
                if player_col is not None:
                    net_id = normalize_net_id(row[player_col])
                else:
                    net_id = normalize_net_id(row.iloc[1])
                if net_id is None:
                    continue
                if net_id not in attendance:
                    attendance[net_id] = 1
                else:
                    attendance[net_id] = attendance[net_id] + 1
    if lecture_num == 0:
        return attendance
    for i in attendance.keys():
        attendance[i] = int(attendance[i] / lecture_num * 100)
    return attendance