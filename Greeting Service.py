from fastapi import FastAPI,HTTPException
from typing import Optional


app = FastAPI()
# below is the name is path parameter and age is query parameter
@app.get("/greet/{name}")
def greet(name: str, age:Optional[int] = None,city:Optional[str] = None):

    if age is not None and age <= 0:
        raise HTTPException(status_code=400, detail="Age must be a positive integer")
        
    if age is None:
        return {"message":f" hello {name.strip()}!"}
        
    return {"message":f" hello {name.strip()}! and your age is {age} you are from {city}"}

# name and age as query parameters here name is required and age is optional

@app.get("/greet_query/")
def greet_with_query(name:str, age:Optional[int] = None,city:Optional[str] = None):

    if age is not None and age <= 0:
        raise HTTPException(status_code=400, detail="Age must be a positive integer")
    
    if age is None:
        return {"message":f" hello {name.strip()}!"}
    
    return {"message":f" hello {name.strip()}! and your age is {age} you are from {city}"}


if __name__ == '__main__':

    import uvicorn
    uvicorn.run('Greeting Service:app', host='127.0.0.1', port=8000,reload=True)