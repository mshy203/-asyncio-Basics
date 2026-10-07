from typing import List, Optional
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

app = FastAPI(title="Task Manager API", version="1.0")

class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    priority: int = Field(1, ge=1, le=4)

class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    priority: Optional[int] = Field(None, ge=1, le=4)
    status: Optional[str] = None

class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    priority: int
    status: str
    xp: int

    class Config:
        from_attributes = True

fake_tasks_db = []
id_counter = 1

@app.post("/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(task_in: TaskCreate):
    global id_counter
    
    calculated_xp = task_in.priority * 15
    
    new_task = {
        "id": id_counter,
        "title": task_in.title,
        "description": task_in.description,
        "priority": task_in.priority,
        "status": "todo",
        "xp": calculated_xp
    }
    
    fake_tasks_db.append(new_task)
    id_counter += 1
    return new_task

@app.get("/tasks", response_model=List[TaskResponse])
def get_tasks():
    return fake_tasks_db

@app.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id: int):
    for task in fake_tasks_db:
        if task["id"] == task_id:
            return task
    raise HTTPException(status_code=404, detail="Завдання не знайдено")

@app.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, task_in: TaskUpdate):
    for task in fake_tasks_db:
        if task["id"] == task_id:
            update_data = task_in.model_dump(exclude_unset=True)
            
            for key, value in update_data.items():
                task[key] = value
                
            if "priority" in update_data:
                task["xp"] = task["priority"] * 15
                
            return task
                
    raise HTTPException(status_code=404, detail="Завдання не знайдено")

@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int):
    for index, task in enumerate(fake_tasks_db):
        if task["id"] == task_id:
            fake_tasks_db.pop(index)
            return
                
    raise HTTPException(status_code=404, detail="Завдання не знайдено")