from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from ..crud import (
    add_student,
    update_student,
    retrieve_students,
    retrieve_student,
    delete_student
)

from ..models.student import (
    ErrorResponseModel,
    ResponseModel,
    StudentSchema,
    UpdateStudentModel
)

router = APIRouter()


@router.post('/', response_description='Student data added into the database')
async def add_student_data(student: StudentSchema = Body(...)):
    student = jsonable_encoder(student)
    new_student = await add_student(student)
    return ResponseModel(new_student, 'Student added successfully')


@router.get('/', response_description='Students retrieved')
async def get_students():
    students = await retrieve_students()
    if students:
        return ResponseModel(students, 'Students data retrieved succes')
    return ResponseModel(students, 'Empty list returned')


@router.get('/{id}/', response_description='Student retrieved')
async def get_student(id):
    student = await retrieve_student(id)
    if student:
        return ResponseModel(student, 'Student retrieved success')
    return ErrorResponseModel('An error occurred', 404, 'Student does not exist.')


@router.put("/{id}")
async def update_student_data(id: str, req: UpdateStudentModel = Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_student = await update_student(id, req)
    if updated_student:
        return ResponseModel(
            "Student with ID: {} name update is successful".format(id),
            "Student name updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the student data.",
    )


@router.delete('/{id}/')
async def delete_student_data(id: str):
    deleted_student = await delete_student(id)
    if deleted_student:
        return ResponseModel(
            f'Student with ID: {id} removed',
            'Student deleted successfully'
        )
    return ErrorResponseModel(
        "An error occurred", 404, f"Student with id {id} doesn't exist"
    )
