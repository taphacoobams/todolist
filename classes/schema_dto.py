from pydantic import BaseModel
from datetime import datetime
from uuid import UUID

class Task(BaseModel):
    id: str  # Identifiant unique de l'annonce
    title: str

class TaskNoId(BaseModel):
    title: str

class User(BaseModel):
    email: str  
    password: str  