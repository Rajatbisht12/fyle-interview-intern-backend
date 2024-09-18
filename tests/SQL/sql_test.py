import random
from sqlalchemy import text

from core import db
from core.models.assignments import Assignment, AssignmentStateEnum, GradeEnum


import random

def create_n_graded_assignments_for_teacher(number: int = 0, teacher_id: int = 1, grade_a_count: int = 0) -> int:
    """
    Creates 'n' graded assignments for a specified teacher and returns the count of assignments with grade 'A'.

    Parameters:
    - number (int): The total number of assignments to be created.
    - teacher_id (int): The ID of the teacher for whom the assignments are created.
    - grade_a_count (int): The number of grade 'A' assignments to ensure are created.

    Returns:
    - int: Count of assignments with grade 'A'.
    """
    # Initial count of existing assignments with grade 'A' for the specified teacher
    existing_grade_a_count: int = Assignment.filter(
        Assignment.teacher_id == teacher_id,
        Assignment.grade == GradeEnum.A
    ).count()

    total_grade_a_count = existing_grade_a_count + grade_a_count

    # Create the specified number of graded assignments
    for _ in range(number):
        # Decide whether to create a grade A assignment based on the specified count
        if grade_a_count > 0:
            grade = GradeEnum.A
            grade_a_count -= 1
        else:
            grade = random.choice(list(GradeEnum))
        
        # Create a new Assignment instance
        assignment = Assignment(
            teacher_id=teacher_id,
            student_id=1,
            grade=grade,
            content='test content',
            state=AssignmentStateEnum.GRADED
        )

        # Add the assignment to the database session
        db.session.add(assignment)

    # Commit changes to the database
    db.session.commit()

    # Return the total count of assignments with grade 'A'
    return total_grade_a_count



def test_get_assignments_in_graded_state_for_each_student():
    """Test to get graded assignments for each student"""

    # Find all the assignments for student 1 and change its state to 'GRADED'
    submitted_assignments: Assignment = Assignment.filter(Assignment.student_id == 1)

    # Iterate over each assignment and update its state
    for assignment in submitted_assignments:
        assignment.state = AssignmentStateEnum.GRADED  # Or any other desired state

    # Flush the changes to the database session
    db.session.flush()
    # Commit the changes to the database
    db.session.commit()

    # Define the expected result before any changes
    expected_result = [(1, 3)]

    # Execute the SQL query and compare the result with the expected result
    with open('tests/SQL/number_of_graded_assignments_for_each_student.sql', encoding='utf8') as fo:
        sql = fo.read()

    # Execute the SQL query compare the result with the expected result
    sql_result = db.session.execute(text(sql)).fetchall()
    for itr, result in enumerate(expected_result):
        assert result[0] == sql_result[itr][0]


def test_get_grade_A_assignments_for_teacher_with_max_grading():
    """Test to get count of grade A assignments for teacher which has graded maximum assignments"""

    with open('tests/SQL/count_grade_A_assignments_by_teacher_with_max_grading.sql', encoding='utf8') as fo:
        sql = fo.read()

    # Create and grade 5 assignments for the default teacher (teacher_id=1), expecting 2 grade A assignments
    grade_a_count_1 = create_n_graded_assignments_for_teacher(5, teacher_id=1, grade_a_count=2)
    print("Grade A Count for Teacher 1 (Expected: 2):", grade_a_count_1)

    # Execute the SQL query and check if the count matches the created assignments
    sql_result = db.session.execute(text(sql)).fetchall()
    actual_grade_a_count = sql_result[0][0]
    print("SQL Result for Teacher 1:", sql_result)
    
    expected_grade_a_count = 2
    assert actual_grade_a_count == expected_grade_a_count

    # Create and grade 10 assignments for a different teacher (teacher_id=2)
    grade_a_count_2 = create_n_graded_assignments_for_teacher(10, teacher_id=2, grade_a_count=2)
    print("Grade A Count for Teacher 2 (Expected: 2):", grade_a_count_2)

    # Execute the SQL query again and check if the count matches the newly created assignments
    sql_result = db.session.execute(text(sql)).fetchall()
    actual_grade_a_count_2 = sql_result[0][0]
    print("SQL Result for Teacher 2:", sql_result)
    
    expected_grade_a_count_2 = 2  # Adjust this value based on the actual grading logic
    assert actual_grade_a_count_2 == expected_grade_a_count_2
