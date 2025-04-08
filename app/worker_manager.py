import asyncio
import json
from typing import Dict, Callable, Optional, List

from app.redis_manager import RedisManager


class WorkerManager(RedisManager):
    def __init__(self):
        super().__init__()
        self._workers: Dict[int, asyncio.Task] = {}
        self._running_workers: Dict[int, bool] = {}
        self._current_tasks: Dict[int, Optional[asyncio.Task]] = {}
        self._next_worker_id = 1

    async def get_task_from_queue(self) -> Optional[Dict]:
        """Getting task from queue."""
        if not self.redis:
            await self.connect()

        task = await self.redis.brpop(self.queue_name, timeout=1)
        if task is None:
            return None
        return json.loads(task[1])

    async def start_worker(self, handler: Callable) -> int:
        worker_id = self._next_worker_id
        self._next_worker_id += 1

        self._running_workers[worker_id] = True
        self._current_tasks[worker_id] = None

        task = asyncio.create_task(
            self._worker_loop(worker_id, handler),
            name=f"worker-{worker_id}"
        )
        self._workers[worker_id] = task
        return worker_id

    async def stop_worker(self, worker_id: int, timeout: float = 30.0) -> bool:
        if worker_id not in self._workers:
            return False

        self._running_workers[worker_id] = False

        current_task = self._current_tasks[worker_id]
        if current_task and not current_task.done():
            current_task.cancel()
            try:
                await asyncio.wait_for(current_task, timeout=timeout)
            except (asyncio.CancelledError, asyncio.TimeoutError):
                pass

        worker_task = self._workers.pop(worker_id)
        try:
            await asyncio.wait_for(worker_task, timeout=timeout)
        except asyncio.TimeoutError:
            worker_task.cancel()
            await asyncio.sleep(0.1)

        self._current_tasks.pop(worker_id, None)
        self._running_workers.pop(worker_id, None)
        return True

    async def stop_all_workers(self, timeout: float = 30.0) -> None:
        workers_to_stop = list(self._workers.keys())
        for worker_id in workers_to_stop:
            await self.stop_worker(worker_id, timeout)

    async def _process_task(self, task: Dict, handler: Callable) -> None:
        try:
            result, error = await handler(
                task['func'], *task['args'], **task['kwargs']
            )
            await self.set_result(task['id'], result, error)
        except Exception as e:
            await self.set_result(task['id'], None, str(e))

    async def _worker_loop(self, worker_id: int, handler: Callable):
        print(f"Worker {worker_id} started")

        try:
            while self._running_workers.get(worker_id, False):
                task = await self.get_task_from_queue()
                if task:
                    task_obj = asyncio.create_task(
                        self._process_task(task, handler)
                    )
                    self._current_tasks[worker_id] = task_obj

                    try:
                        await task_obj
                    except asyncio.CancelledError:
                        await self.set_result(
                            task['id'],
                            None,
                            "Task cancelled due to worker shutdown"
                        )
                        raise
                    except Exception as e:
                        print(f"Worker {worker_id} task failed: {e}")
                    finally:
                        self._current_tasks[worker_id] = None
                else:
                    await asyncio.sleep(0.1)
        except asyncio.CancelledError:
            print(f"Worker {worker_id} received cancellation signal")
        finally:
            print(f"Worker {worker_id} stopped")
            self._running_workers.pop(worker_id, None)
            self._current_tasks.pop(worker_id, None)

    def get_worker_ids(self) -> List[int]:
        return list(self._workers.keys())
