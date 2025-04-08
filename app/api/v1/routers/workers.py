import asyncio
from typing import List

from fastapi import APIRouter, HTTPException

from app.schemas.worker import WorkerResponse
from app.handler import task_handler
from app.worker_manager import WorkerManager

router = APIRouter()
manager = WorkerManager()


@router.post("/start_worker", response_model=WorkerResponse)
async def start():
    worker_id = await asyncio.create_task(
        manager.start_worker(
            handler=task_handler,
        )
    )
    return WorkerResponse(number=worker_id, status="creating")


@router.delete("/stop_worker/{worker_id}", response_model=WorkerResponse)
async def stop(worker_id: int):
    status = await manager.stop_worker(worker_id)
    if status is False:
        raise HTTPException(status_code=404, detail="Worker not found")

    return WorkerResponse(number=worker_id, status="stopped")

@router.post("/stop-all")
async def stop_all_workers():
    await manager.stop_all_workers()
    return {"status": "all workers stopped"}

@router.get("/workers", response_model=List[WorkerResponse])
async def list_workers():
    return [{"id": wid, "status": "running"} for wid in manager.get_worker_ids()]
