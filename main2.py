import asyncio
import logging
from typing import Any, Dict, List, Optional

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

BASE_URL: str = "https://jsonplaceholder.typicode.com/todos"

async def get_tasks() -> Optional[List[Dict[str, Any]]]:
    logging.info("Отримання списку всіх задач...")
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(BASE_URL, timeout=5.0)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            logging.error(f"error: {e.response.status_code}")
        except httpx.RequestError as e:
            logging.error(f"error: {e}")
        return None

# 2. GET — отримати одну задачу за ID (з можливістю спіймати 404)
async def get_task_by_id(task_id: int) -> Optional[Dict[str, Any]]:
    url = f"{BASE_URL}/{task_id}"
    logging.info(f"Отримання задачі з ID: {task_id}")
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, timeout=5.0)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                logging.warning(f"Задачу з ID {task_id} не знайдено (Статус 404).")
            else:
                logging.error(f"HTTP помилка: {e.response.status_code}")
        except httpx.RequestError as e:
            logging.error(f"Помилка мережі: {e}")
        return None