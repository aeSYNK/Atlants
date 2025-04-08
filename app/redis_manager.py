import asyncio
import json
from typing import Any, Optional, Dict

import redis.asyncio as redis


class RedisManager:
    def __init__(
            self,
            redis_url: str = "redis://redis:6379/0",
            result_ttl: int = 3600,
            queue_name: str = "task_queue",
            ):
        self.redis_url = redis_url
        self.result_ttl = result_ttl
        self.redis = None
        self.queue_name: str = "task_queue"
        self.result_prefix = f"{queue_name}_result:"

    async def connect(self) -> None:
        """Connect to Redis."""
        self.redis = redis.from_url(self.redis_url)

    async def disconnect(self) -> None:
        """Disconnect from Redis."""
        if self.redis:
            await self.redis.close()

    async def set_result(
            self,
            task_id: str,
            result: Any = None,
            error: Optional[str] = None
            ) -> None:
        """
        Saving task result.

        :param task_id: ID
        :param result: Result
        :param error: Error
        """
        result_data = {
            "status": "failed" if error else "completed",
            "result": result,
            "error": error,
            "timestamp": asyncio.get_event_loop().time()
        }

        print(f"Result from task: {task_id}", result)

        await self.redis.set(
            f"{self.result_prefix}{task_id}",
            json.dumps(result_data),
            ex=self.result_ttl
        )

    async def get_result(self, task_id: str) -> Optional[Dict]:
        """
        Getting task results.

        :param task_id: task ID
        :return: Результат или None если задача не завершена
        """
        if not self.redis:
            await self.connect()

        result = await self.redis.get(f"{self.result_prefix}{task_id}")
        return json.loads(result) if result else None
