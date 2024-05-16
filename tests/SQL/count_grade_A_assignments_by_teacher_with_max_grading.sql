-- Write query to find the number of grade A's given by the teacher who has graded the most assignments
SELECT u.id AS teacher_id, COUNT(CASE WHEN a.grade = 'A' THEN 1 END) AS grade_A_count 
FROM Assignments a JOIN Users u ON a.teacher_id = u.id GROUP BY u.id 
ORDER BY grade_A_count DESC LIMIT 1;