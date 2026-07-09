from tasks.day01_greeting import router as greeting_router
from tasks.day02_product_catalog import router as product_router
from tasks.day03_Student_Management_API import router as student_router
from tasks.day04_Employee_Management_CRUD import router as employee_router
from fastapi import FastAPI

app = FastAPI(
    title="FastAPI Practice",
    version="1.0.0",
)


app.include_router(greeting_router)
app.include_router(product_router)
app.include_router(student_router)
app.include_router(employee_router)
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )

