import asyncio

from app.tasks import task_manager


async def task_handler(func_name: str, *args, **kwargs):
    try:
        task_func = task_manager.get_task(func_name)
        result = await asyncio.wait_for(
            task_func(*args, **kwargs),
            timeout=30.0
        )
        print(f"Task '{func_name}' completed successfully")
        return result, None
    except asyncio.TimeoutError:
        error_msg = f"Task '{func_name}' timed out"
        return {"status": "failed", "message": error_msg}, "Timeout"

    except Exception as e:
        error_msg = f"Task '{func_name}' failed: {str(e)}"
        return {"status": "failed", "message": error_msg}, str(e)
