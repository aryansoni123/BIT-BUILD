import subprocess
import psycopg2
from datetime import datetime

# ---------- Data / constants (unchanged) ----------
TEACHER_CREDENTIALS = {
    "DMS": ("DMS_teacher", "passDMS"),
    "COA": ("COA_teacher", "passCOA"),
    "TOC": ("TOC_teacher", "passTOC"),
    "DBMS": ("DBMS_teacher", "passDBMS"),
    "OOPSJ": ("OOPSJ_teacher", "passOOPSJ"),
    "LMP-2": ("LMP2_teacher", "passLMP2"),
    "LOOPSJ": ("LOOPSJ_teacher", "passLOOPSJ"),
    "LCOA": ("LCOA_teacher", "passLCOA"),
    "LDBMS": ("LDBMS_teacher", "passLDBMS")
}
EXPECTED_WIFI = "Mayank"
CSV_FILE = "attendance.csv"

students = {
    "11": ("Arin", "arin"),
    "28": ("Mayank", "mayank"),
    "19": ("Gatik", "gatik"),
}

SUBJECTS = ["DMS", "COA", "TOC", "DBMS", "OOPSJ", "LMP-2", "LOOPSJ", "LCOA", "LDBMS"]

# Database connection parameters
DB_CONFIG = {
    "dbname": "Attendance",
    "user": "postgres",
    "password": "123654",
    "host": "localhost",
    "port": "5432"
}

def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)

def get_wifi_ssid():
    """Call netsh and parse output (unchanged logic)."""
    try:
        result = subprocess.check_output(
            "netsh wlan show interfaces", shell=True
        ).decode("utf-8", errors="ignore")
        for line in result.split("\n"):
            if "SSID" in line and ":" in line:
                return line.split(":", 1)[1].strip()
    except Exception as e:
        print("Error getting WiFi SSID:", e)
    return None


def update_attendance(student_name, subject):
    """Mark attendance in PostgreSQL database"""
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                # Get student_id
                cur.execute("SELECT student_id FROM Students WHERE name = %s", (student_name,))
                student_result = cur.fetchone()
                if not student_result:
                    return False
                student_id = student_result[0]

                # Get active session for the class
                cur.execute("""
                    SELECT s.session_id 
                    FROM Sessions s
                    JOIN Classes c ON s.class_id = c.class_id
                    WHERE c.class_name = %s AND s.is_active = TRUE
                    AND NOW() BETWEEN s.start_time AND s.end_time
                """, (subject,))
                session_result = cur.fetchone()
                if not session_result:
                    return False
                session_id = session_result[0]

                # Insert attendance record
                try:
                    cur.execute("""
                        INSERT INTO Attendance (session_id, student_id, marked_at)
                        VALUES (%s, %s, CURRENT_TIMESTAMP)
                    """, (session_id, student_id))
                    conn.commit()
                    return True
                except psycopg2.IntegrityError:
                    # Attendance already marked
                    return False
    except Exception as e:
        print(f"Error marking attendance: {e}")
        return False

def get_student_attendance(student_name):
    """Get attendance summary for a student"""
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT c.class_name, COUNT(a.attendance_id) as attended_classes
                    FROM Students s
                    JOIN Enrollments e ON s.student_id = e.student_id
                    JOIN Classes c ON e.class_id = c.class_id
                    LEFT JOIN Sessions ses ON c.class_id = ses.class_id
                    LEFT JOIN Attendance a ON ses.session_id = a.session_id 
                        AND a.student_id = s.student_id
                    WHERE s.name = %s
                    GROUP BY c.class_name
                """, (student_name,))
                return cur.fetchall()
    except Exception as e:
        print(f"Error getting attendance: {e}")
        return []

def get_all_attendance():
    """Get attendance for all students"""
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT s.name, c.class_name, COUNT(a.attendance_id) as attended_classes
                    FROM Students s
                    JOIN Enrollments e ON s.student_id = e.student_id
                    JOIN Classes c ON e.class_id = c.class_id
                    LEFT JOIN Sessions ses ON c.class_id = ses.class_id
                    LEFT JOIN Attendance a ON ses.session_id = a.session_id 
                        AND a.student_id = s.student_id
                    GROUP BY s.name, c.class_name
                    ORDER BY s.name, c.class_name
                """)
                return cur.fetchall()
    except Exception as e:
        print(f"Error getting all attendance: {e}")
        return []

# def ensure_attendance_csv():
#     """Create CSV with zeroed subjects if missing (unchanged behavior)."""
#     if not os.path.exists(CSV_FILE):
#         data = []
#         for sid, (name, _) in students.items():
#             row = {"Name": name}
#             for subj in SUBJECTS:
#                 row[subj] = 0
#             data.append(row)
#         df = pd.DataFrame(data)
#         df.to_csv(CSV_FILE, index=False)
#         print("Created new attendance.csv")
