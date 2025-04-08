import json
import uuid
from typing import Dict, Callable, Optional

from app.redis_manager import RedisManager


class TaskQueueManager(RedisManager):
    def __init__(self):
        super().__init__()
        self._tasks: Dict[str, Callable] = {}

    async def enqueue(self, func_name: str, *args, **kwargs) -> str:
        """
        Adding task to the queue.

        :param func_name: func name
        :param args: args
        :param kwargs: kwargs
        :return: task_id
        """
        if not self.redis:
            await self.connect()

        task_id = str(uuid.uuid4())
        task_data = {
            "id": task_id,
            "func": func_name,
            "args": args,
            "kwargs": kwargs
        }
        await self.redis.lpush(self.queue_name, json.dumps(task_data))
        return task_id

    def get_task(self, name: str) -> Callable:
        """Getting registered task."""
        if name not in self._tasks:
            raise ValueError(f"Task '{name}' not registered")
        return self._tasks[name]

    def task(self, name: Optional[str] = None):
        """Decorator to create a task class out of any callable."""
        def decorator(fn):
            task_name = name or fn.__name__
            self._tasks[task_name] = fn
            return fn
        return decorator
