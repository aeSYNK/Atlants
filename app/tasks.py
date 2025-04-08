import asyncio
from datetime import datetime

from app.queue_manager import TaskQueueManager


task_manager = TaskQueueManager()


@task_manager.task("send_email")
async def send_email(to: str, subject: str, body: str) -> dict:
    print(f"[{datetime.now()}] Sending email to {to}: {subject}")
    await asyncio.sleep(7)
    return {"status": "sent", "to": to, "subject": subject}

@task_manager.task("process_image")
async def process_image(image_path: str) -> dict:
    print(f"[{datetime.now()}] Processing image: {image_path}")
    await asyncio.sleep(5)
    return {"status": "processed", "path": image_path}

@task_manager.task("fail_task")
async def fail_task() -> dict:
    print(f"[{datetime.now()}] Fail task")
    await asyncio.sleep(3)
    raise KeyError()
