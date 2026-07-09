
from fastapi import HTTPException, APIRouter
from pydantic import BaseModel, Field
from typing import Optional, Annotated

router = APIRouter(
    prefix="/employees",
    tags=["Employees"]
)
employees = []
class EmployeeCreate(BaseModel):

    name: Annotated[str, Field(min_length=3)]
    age: Annotated[int, Field(ge=18, le=65)]
    department: Annotated[str, Field(min_length=2)]
    salary: Annotated[float, Field(gt=0)]

class EmployeeResponse(BaseModel):
    id: int
    name: str
    age: int
    department: str
    salary: float

class EmployeeUpdate(BaseModel):
    name: Optional[Annotated[str, Field(min_length=3)]] = None
    age: Optional[Annotated[int, Field(ge=18, le=65)]] = None
    department: Optional[Annotated[str, Field(min_length=2)]] = None
    salary: Optional[Annotated[float, Field(gt=0)]] = None


@router.post("/",response_model=EmployeeResponse)
def create_employee(employee: EmployeeCreate):

    employee_id = len(employees) + 1
    # employee_data = {
    #     "id": employee_id,
    #     "name": employee.name,
    #     "age": employee.age,
    #     "department": employee.department,
    #     "salary": employee.salary,
    #     "default": "This field is not included in the response and is critical"
    # }
    employee_data = employee.dict()
    employee_data["id"] = employee_id
    # print(f"Creating employee: {employee_data}")
    employees.append(employee_data)
    print(employees)
    return EmployeeResponse(**employee_data)


@router.get("/", response_model=list[EmployeeResponse])
def get_employees():
    if not employees:
        raise HTTPException(status_code=404, detail="No employees found")
    return employees
    
    

@router.get("/{employee_id}")
def get_employee(employee_id: int):
    
    # filtered_employess=[employee for employee in employees if employee["id"] == employee_id]
    filtered_employes = next((employee for employee in employees if employee["id"] == employee_id), None)
    if not filtered_employes:
        raise HTTPException(status_code=404, detail="Employee not found")
    return EmployeeResponse(**filtered_employes)

@router.put("/{employee_id}", response_model=EmployeeResponse)
def update_employee(employee_id: int, employee: EmployeeCreate):
    
    for index, existing_employee in enumerate(employees):
        if existing_employee["id"] == employee_id:
            updated_employee = existing_employee.copy()
            updated_employee.update(employee.dict())
            employees[index] = updated_employee
            return EmployeeResponse(**updated_employee)
        
@router.patch("/{employee_id}")
def partial_update_employee(employee_id: int, employee: EmployeeUpdate):
    

    for index, existing_employee in enumerate(employees):
        if existing_employee["id"] == employee_id:
            updated_employee = existing_employee.copy()
            update_data = employee.dict(exclude_unset=True)
            print(f"Updating employee with ID {employee_id}: {update_data}")
            updated_employee.update(update_data)
            print(f"Updated employee data: {updated_employee}")
            employees[index] = updated_employee
            return EmployeeResponse(**updated_employee)


@router.delete("/{employee_id}")
def delete_employee(employee_id: int):
    
    # deleted_employee = [employee for employee in employees if employee["id"] == employee_id]
    # if not deleted_employee:
    #     raise HTTPException(status_code=404, detail="Employee not found")
    # employees.remove(deleted_employee[0])


    deleted_employee = next((employee for employee in employees if employee["id"] == employee_id), None)
    if not deleted_employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    if deleted_employee:
        employees.remove(deleted_employee)
        return {
            "message": "Employee deleted successfully"
        }
    
    # for index, employee in enumerate(employees):
    #     if employee["id"] == employee_id:
    #         del employees[index]
    #         return {
    #             "message": "Employee deleted successfully"
    #         }

