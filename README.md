# course-kahoot-backend

Instructions:
1. Clone this repo
2. Use Python 3.11+ (3.12 recommended), create a virtual environment, and install packages from `requirements.txt`
3. In the same directory as `app.py`, create `students.txt` with all students' netids, one per line
4. On Kahoot, download each report from [kahoot.com](https://kahoot.com/) &rarr; Reports &rarr; `Download Report`
5. Rename each downloaded report to `lecture<lecture number>.xlsx` (for example, `lecture1.xlsx`, `lecture2.xlsx`) and place it in the same directory as `app.py`
6. Run the server:
   - Local: `python app.py`
   - Docker: `docker build -t course-kahoot-backend . && docker run -p 5000:5000 course-kahoot-backend`
