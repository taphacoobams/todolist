from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, List
from uuid import UUID, uuid4
from classes.schema_dto import Task, TaskNoId
from database.firebse import db
from routers.routers_auth import get_current_user
import uuid

router = APIRouter(
    prefix='/task',
    tags=["task"]
)


@router.post('/', response_model=Task, status_code=201)
async def add_new_task(given_task: TaskNoId, userData: int = Depends(get_current_user)):
    # Générez un ID unique pour la tâche
    generated_id = uuid4()
    
    # Créez une nouvelle instance de la tâche
    new_task = Task(
        id=str(generated_id),
        title=given_task.title,
    )

    # Ajoutez la nouvelle tâche à la base de données Firebase
    db.child("tasks").child(str(generated_id)).set(new_task.model_dump(), userData['idToken'])
    return new_task

@router.get('/', response_model=List[Task])
async def get_all_tasks(userData: int = Depends(get_current_user)):
    tasks_data = db.child("tasks").get(userData['idToken']).val()
    if tasks_data:
        # Si des données sont disponibles, convertissez-les en une liste de tâches
        tasks_list = []
        for task_id, task_data in tasks_data.items():
            task = Task(id=task_id, title=task_data["title"])
            tasks_list.append(task)
        return tasks_list
    else:
        return []

@router.get('/{task_id}', response_model=Task)
async def get_task_by_id(task_id: str, userData: int = Depends(get_current_user)):
    task_data = db.child("tasks").child(task_id).get(userData['idToken']).val()
    if task_data:
        return task_data
    else:
        raise HTTPException(status_code=404, detail="Task not found")

@router.delete('/{task_id}', response_model=dict)
async def delete_task_by_id(task_id: str, userData: int = Depends(get_current_user)):
    task_data = db.child("tasks").child(task_id).get(userData['idToken']).val()
    if task_data:
        # Supprimez la tâche de la base de données Firebase
        db.child("tasks").child(task_id).remove()
        return {"message": "Task deleted"}
    else:
        raise HTTPException(status_code=404, detail="Task not found")

@router.patch('/{task_id}', response_model=Task)
async def update_task_by_id(task_id: str, updated_task: TaskNoId, userData: int = Depends(get_current_user)):
    task_data = db.child("tasks").child(task_id).get(userData['idToken']).val()
    if task_data:
        # Mettez à jour partiellement la tâche dans la base de données Firebase
        update_data = {
            "title": updated_task.title,
        }
        db.child("tasks").child(task_id).update(update_data)
        
        updated_task_data = db.child("tasks").child(task_id).get(userData['idToken']).val()
        updated_task = Task(**updated_task_data)
        return updated_task
    else:
        raise HTTPException(status_code=404, detail="Task not found")
