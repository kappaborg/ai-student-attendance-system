"""Student service for the application."""

from ..database.student_model import (
    get_student as db_get_student,
    get_students as db_get_students,
    create_student as db_create_student,
    update_student as db_update_student
)

def get_students():
    """Get all students.
    
    Returns:
        list: List of all students
    """
    students = db_get_students()
    
    # Never return sensitive data to the client
    return sanitize_students(students)

def get_student(student_id):
    """Get a student by ID.
    
    Args:
        student_id (str): The student ID
        
    Returns:
        dict: Student object if found, None otherwise
    """
    student = db_get_student(student_id)
    if not student:
        return None
    
    # Never return sensitive data to the client
    return sanitize_student(student)

def create_student(student_data):
    """Create a new student.
    
    Args:
        student_data (dict): Student data including first_name, last_name, etc.
        
    Returns:
        dict: Result of the operation with success status and message
    """
    # Validate required fields
    required_fields = ['first_name', 'last_name', 'email']
    for field in required_fields:
        if field not in student_data or not student_data[field]:
            return {
                'success': False,
                'message': f'Missing required field: {field}'
            }
    
    # Create student
    new_student = db_create_student(student_data)
    
    if not new_student:
        return {
            'success': False,
            'message': 'Failed to create student. Student may already exist.'
        }
    
    # Never return sensitive data to the client
    return {
        'success': True,
        'message': 'Student created successfully',
        'student': sanitize_student(new_student)
    }

def update_student(student_id, updates):
    """Update a student.
    
    Args:
        student_id (str): The student ID
        updates (dict): Field updates for the student
        
    Returns:
        dict: Result of the operation with success status and message
    """
    # Validate student exists
    student = db_get_student(student_id)
    if not student:
        return {
            'success': False,
            'message': f'Student with ID {student_id} not found'
        }
    
    # Update student
    updated_student = db_update_student(student_id, updates)
    
    if not updated_student:
        return {
            'success': False,
            'message': 'Failed to update student'
        }
    
    # Never return sensitive data to the client
    return {
        'success': True,
        'message': 'Student updated successfully',
        'student': sanitize_student(updated_student)
    }

def sanitize_student(student):
    """Remove sensitive data from student object.
    
    Args:
        student (dict): Student object
        
    Returns:
        dict: Sanitized student object
    """
    # Make a copy to avoid modifying the original
    sanitized = {**student}
    
    # Remove sensitive fields if they exist
    sensitive_fields = []
    for field in sensitive_fields:
        if field in sanitized:
            del sanitized[field]
    
    return sanitized

def sanitize_students(students):
    """Remove sensitive data from a list of student objects.
    
    Args:
        students (list): List of student objects
        
    Returns:
        list: List of sanitized student objects
    """
    return [sanitize_student(student) for student in students] 