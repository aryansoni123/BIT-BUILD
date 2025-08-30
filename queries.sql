-- ======================================================
-- ERP Attendance Database Schema
-- ======================================================

-- ---------- 1. Teachers ----------
CREATE TABLE Teachers (
    teacher_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL
);

-- ---------- 2. Students ----------
CREATE TABLE Students (
    student_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    roll_no VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL
);

-- ---------- 3. Classes ----------
CREATE TABLE Subjects (
    subject_id SERIAL PRIMARY KEY,
    subject_name VARCHAR(100) NOT NULL,
    teacher_id INT NOT NULL,
    FOREIGN KEY (teacher_id) REFERENCES Teachers(teacher_id)
);

-- ---------- 4. Ongoing_classes (Timestamp <-> Classes) ----------
CREATE TABLE Ongoing_classes (
	ongoing_class_id SERIAL PRIMARY KEY,
	subject_id INT NOT NULL,
	total_class_completed INT,
	marked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	FOREIGN KEY (subject_id) REFERENCES Subjects(subject_id)
);

-- ---------- 5. Attendance ----------
CREATE TABLE Attendance (
    attendance_id SERIAL PRIMARY KEY,
    subject_id INT NOT NULL,
    student_id INT NOT NULL,
    marked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (subject_id) REFERENCES Subjects(subject_id),
    FOREIGN KEY (student_id) REFERENCES Students(student_id)
);


-- ======================================================
-- SAMPLE QUERIES
-- ======================================================
/*
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
  */

-- (If the above insert fails = invalid or expired QR)



-- QUERY FOR UPDATING THE ONGOING_CLASSES TABLE 
1.
/*
SELECT total_class_completed FROM Ongoing_classes 
'INSERT INTO Ongoing_classes (subject_id, total_class_completed, marked_at) 
   VALUES ($1, $2, CURRENT_TIMESTAMP)' ,
   [req.user.subject_id, totalCompleted + 1]
   */

   await db.query(
  "UPDATE Ongoing_classes SET subject_id = $1, total_class_completed = total_class_completed + 1, marked_at = CURRENT_TIMESTAMP",
  [newSubjectId]
);




-- MARKING ATTENDANCE BY SCANNING QR_CODE
2.

/*
const query = `
  INSERT INTO Attendance (subject_id, student_id, marked_at)
  SELECT $1, $2, NOW()
  FROM Ongoing_classes oc
  WHERE oc.subject_id = $1
    AND NOW() BETWEEN oc.marked_at AND oc.marked_at + INTERVAL '1 hour';
`;

await db.query(query, [subjectId, studentId]);
*/

INSERT INTO Attendance (subject_id, student_id, marked_at)
SELECT 2, 4, NOW()
FROM Ongoing_classes oc
WHERE oc.subject_id = 2
  AND NOW() BETWEEN oc.marked_at AND oc.marked_at + INTERVAL '1 hour';