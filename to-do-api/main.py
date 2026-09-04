from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class TaskCreate(BaseModel):
    title: str | None = None

tasks = [
    {
        "id": 1,
        "title": "complete assignment",
        "done": False
    },
    {
        "id": 2,
        "title": "Go to gym",
        "done": False
    },
    {
        "id": 3,
        "title": "daily leetcode",
        "done": False
    }
]

@app.get("/")
def home():
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks"]
    }


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/tasks")
def get_tasks():
    return tasks


@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task

    raise HTTPException(
        status_code=404,
        detail=f"Task {task_id} not found"
    )


@app.post("/tasks", status_code=201)
def create_task(task_data: TaskCreate):
    if task_data.title is None or not task_data.title.strip():
        raise HTTPException(
            status_code=400,
            detail="Title is required and cannot be empty"
        )

    new_id = max(task["id"] for task in tasks) + 1

    new_task = {
        "id": new_id,
        "title": task_data.title,
        "done": False
    }

    tasks.append(new_task)

    return new_task