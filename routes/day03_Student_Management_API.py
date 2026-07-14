from fastapi import Query, HTTPException, APIRouter
from typing import Optional, Literal, Annotated 
from pydantic import BaseModel, Field

router = APIRouter(
    prefix="/students",
    tags=["Students"]
)

students = []

class Student(BaseModel):
    name: Annotated[str, Field(min_length=3)]
    # ge means greater than or equal to and gt means greater than and le means less than or equal to and lt means less than
    age: Annotated[int, Field(ge=18, le=60)]
    course: Annotated[str, Field(min_length=2)]


class StudentResponse(BaseModel):
    id: int
    name: str
    age: int
    course: str


@router.post("/",response_model = StudentResponse)
def add_student(student: Student):
    try:
        student_id = len(students) + 1
        student_data = {
            "id": student_id,
            "name": student.name,
            "age": student.age,
            "course": student.course,
            "default": "I do not want to be included in the response and it is critical filed"
        }
        students.append(student_data)
        return StudentResponse(**student_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model= list[StudentResponse])
def get_students():

    if not students:
        raise HTTPException(status_code=404, detail="No students found")
    return students




@router.get("/{student_id}")
def get_student(student_id: int):
    if student_id <= 0:
        raise HTTPException(status_code=400, detail="Invalid student ID")
    filtered_students = [student for student in students if student["id"] == student_id]
    if not filtered_students:
        raise HTTPException(status_code=404, detail="Student not found")
    return StudentResponse(**filtered_students[0])




# 9. Bonus Challenges
# ⭐ Bonus 1

# Add:

# DELETE /students/{student_id}

# Return a success message after deleting.

# ⭐ Bonus 2

# Add:

# PUT /students/{student_id}

# Update all student details.

# ⭐ Bonus 3

# Prevent duplicate students.

# A duplicate is someone with the same:

# Name
# Course

# Think about where this validation belongs.

# ⭐ Bonus 4

# Sort students alphabetically by name when returning all students.