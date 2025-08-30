-- ======================================================
-- ERP Attendance Database Schema
-- ======================================================

-- ---------- 1. Teachers ----------
CREATE TABLE Teachers (
    teacher_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL
);

-- ---------- 2. Students ----------
CREATE TABLE Students (
    student_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    roll_no VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL
);

-- ---------- 3. Classes ----------
CREATE TABLE Classes (
    class_id INT AUTO_INCREMENT PRIMARY KEY,
    class_name VARCHAR(100) NOT NULL,
    teacher_id INT NOT NULL,
    FOREIGN KEY (teacher_id) REFERENCES Teachers(teacher_id)
);

-- ---------- 4. Enrollments (Students <-> Classes) ----------
CREATE TABLE Enrollments (
    enrollment_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    class_id INT NOT NULL,
    FOREIGN KEY (student_id) REFERENCES Students(student_id),
    FOREIGN KEY (class_id) REFERENCES Classes(class_id),
    UNIQUE(student_id, class_id)
);

-- ---------- 5. Sessions (QR linked to class occurrence) ----------
CREATE TABLE Sessions (
    session_id INT AUTO_INCREMENT PRIMARY KEY,
    class_id INT NOT NULL,
    session_date DATE NOT NULL,
    start_time DATETIME NOT NULL,
    end_time DATETIME NOT NULL,
    qr_token VARCHAR(255) UNIQUE NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (class_id) REFERENCES Classes(class_id)
);

-- ---------- 6. Attendance ----------
CREATE TABLE Attendance (
    attendance_id INT AUTO_INCREMENT PRIMARY KEY,
    session_id INT NOT NULL,
    student_id INT NOT NULL,
    marked_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (session_id) REFERENCES Sessions(session_id),
    FOREIGN KEY (student_id) REFERENCES Students(student_id),
    UNIQUE(session_id, student_id)
);

-- ======================================================
-- SAMPLE QUERIES
-- ======================================================

-- 1. Teacher: View attendance for a class
-- Shows each student and whether attended in a given session
SELECT s.name, a.session_id, a.marked_at
FROM Students s
JOIN Attendance a ON s.student_id = a.student_id
JOIN Sessions se ON a.session_id = se.session_id
WHERE se.class_id = 1;

-- 2. Student: View own attendance across subjects
SELECT c.class_name, COUNT(a.attendance_id) AS attended_classes
FROM Classes c
JOIN Sessions se ON c.class_id = se.class_id
LEFT JOIN Attendance a ON se.session_id = a.session_id AND a.student_id = 1
GROUP BY c.class_id, c.class_name;

-- 3. Mark attendance (validates QR + expiry)
INSERT INTO Attendance (session_id, student_id)
SELECT se.session_id, 1
FROM Sessions se
WHERE se.qr_token = 'xyz123'
  AND NOW() BETWEEN se.start_time AND se.end_time
  AND se.is_active = TRUE;

-- (If the above insert fails = invalid or expired QR)
