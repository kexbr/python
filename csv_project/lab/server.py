import os
from typing import List, Optional
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

from . import processing
from . import io_utils
from .models import Student
from .errors import AppError, NotFoundError, DuplicateError

app = FastAPI(title="Students API")

DATA_FILE = "data/students.csv"
students_list: List[Student] = []

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

class StudentCreate(BaseModel):
    id: int
    name: str
    grades: List[Optional[int]]

@app.on_event("startup")
def startup_event():
    global students_list
    if os.path.exists(DATA_FILE):
        students_list = io_utils.read_csv(DATA_FILE, has_header=True)

def save_db():
    os.makedirs("data", exist_ok=True)
    io_utils.write_csv(DATA_FILE, students_list)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)

@app.get("/api/students")
def get_students():
    return [{"id": s.id, "name": s.name, "grades": s.grades, "average": s.average} for s in students_list]

@app.post("/api/students")
async def add_student(student_in: StudentCreate):
    new_student = Student(id=student_in.id, name=student_in.name, grades=student_in.grades)
    try:
        processing.add_student(students_list, new_student)
        save_db()
        await manager.broadcast("update")
        return {"message": "Студент добавлен"}
    except DuplicateError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/api/students/{student_id}")
async def delete_student(student_id: int):
    try:
        processing.remove_student(students_list, student_id)
        save_db()
        await manager.broadcast("update")
        return {"message": "Студент удален"}
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.get("/api/stats")
def get_stats():
    stats = processing.get_statistics(students_list)
    return {
        "count": stats["count"],
        "overall_avg": stats["overall_avg"],
        "best": stats["best"].name if stats["best"] else None,
        "worst": stats["worst"].name if stats["worst"] else None,
    }

app.mount("/static", StaticFiles(directory="public"), name="static")

@app.get("/")
def read_root():
    """Публичная страница (только чтение)"""
    return FileResponse("public/index.html")

@app.get("/admin")
def read_admin():
    """Панель администратора (редактирование)"""
    return FileResponse("public/admin.html")