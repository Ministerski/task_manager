from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlmodel import Session

from app.core.dependencies import get_current_user_id
from app.db.database import get_session
from app.models.models import TaskStatus, TaskPriority
from app.schemas.task import TaskCreate, TaskUpdate, TaskRead
from app.services.task_service import TaskService

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post("/", response_model=TaskRead, status_code=201)
def create_task(
    data: TaskCreate,
    owner_id: int = Depends(get_current_user_id),
    session: Session = Depends(get_session),
):
    """Создать новую задачу."""
    return TaskService.create_task(session, data, owner_id)


@router.get("/", response_model=List[TaskRead])
def list_tasks(
    task_status: Optional[TaskStatus] = Query(default=None, description="Фильтр по статусу"),
    priority: Optional[TaskPriority] = Query(default=None, description="Фильтр по приоритету"),
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=500),
    owner_id: int = Depends(get_current_user_id),
    session: Session = Depends(get_session),
):
    """Получить список своих задач (с фильтрацией по статусу и приоритету)."""
    return TaskService.list_tasks(session, owner_id, task_status, priority, offset, limit)


@router.get("/{task_id}", response_model=TaskRead)
def get_task(
    task_id: int,
    owner_id: int = Depends(get_current_user_id),
    session: Session = Depends(get_session),
):
    """Получить задачу по ID."""
    return TaskService.get_task(session, task_id, owner_id)


@router.put("/{task_id}", response_model=TaskRead)
def update_task(
    task_id: int,
    data: TaskUpdate,
    owner_id: int = Depends(get_current_user_id),
    session: Session = Depends(get_session),
):
    """Обновить задачу."""
    return TaskService.update_task(session, task_id, owner_id, data)


@router.delete("/{task_id}", status_code=204)
def delete_task(
    task_id: int,
    owner_id: int = Depends(get_current_user_id),
    session: Session = Depends(get_session),
):
    """Удалить задачу."""
    TaskService.delete_task(session, task_id, owner_id)
