from fastapi import FastAPI
from app.api.v1 import task_router, task_worker

app = FastAPI(title="Async Task Queue")


app.include_router(task_router, prefix="/tasks")
app.include_router(task_worker, prefix="/workers")
