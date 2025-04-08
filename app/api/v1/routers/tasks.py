from fastapi import APIRouter

from app.schemas.task import TaskCreate
from app.tasks import task_manager

router = APIRouter()


@router.get("/email_task", response_model=TaskCreate)
async def email_task():
    task_id = await task_manager.enqueue(
        "send_email",
        "user@example.com",
        "Hello from AsyncQueue",
        "This is a test email"
    )
    return TaskCreate(task_id=task_id, status="queued")

@router.get("/image_task")
async def image_task():
    task_id = await task_manager.enqueue(
        "process_image",
        "/path/to/image.jpg"
    )
    return TaskCreate(task_id=task_id, status="queued")


@router.get("/failed_task")
async def failed_task():
    task_id = await task_manager.enqueue("fail_task")
    return TaskCreate(task_id=task_id, status="queued")

