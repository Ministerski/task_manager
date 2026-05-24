from datetime import datetime, timezone
from typing import List, Optional

from fastapi import HTTPException, status
from sqlmodel import Session, select

from app.models.models import Task, TaskStatus, TaskPriority
from app.schemas.task import TaskCreate, TaskUpdate


class TaskService:

    @staticmethod
    def create_task(session: Session, data: TaskCreate, owner_id: int) -> Task:
        task = Task(**data.model_dump(), owner_id=owner_id)
        session.add(task)
        session.commit()
        session.refresh(task)
        return task

    @staticmethod
    def get_task(session: Session, task_id: int, owner_id: int) -> Task:
        task = session.get(Task, task_id)
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Task with id={task_id} not found.",
            )
        if task.owner_id != owner_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied.",
            )
        return task

    @staticmethod
    def list_tasks(
        session: Session,
        owner_id: int,
        task_status: Optional[TaskStatus] = None,
        priority: Optional[TaskPriority] = None,
        offset: int = 0,
        limit: int = 100,
    ) -> List[Task]:
        query = select(Task).where(Task.owner_id == owner_id)
        if task_status:
            query = query.where(Task.status == task_status)
        if priority:
            query = query.where(Task.priority == priority)
        query = query.offset(offset).limit(limit)
        return session.exec(query).all()

    @staticmethod
    def update_task(
        session: Session,
        task_id: int,
        owner_id: int,
        data: TaskUpdate,
    ) -> Task:
        task = TaskService.get_task(session, task_id, owner_id)
        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(task, key, value)
        task.updated_at = datetime.now(timezone.utc)
        session.add(task)
        session.commit()
        session.refresh(task)
        return task

    @staticmethod
    def delete_task(session: Session, task_id: int, owner_id: int) -> None:
        task = TaskService.get_task(session, task_id, owner_id)
        session.delete(task)
        session.commit()
