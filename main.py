import asyncio
import logging
import httpx
from typing import Any, Dict, List, Optional

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

BASE_URL: str = "https://jsonplaceholder.typicode.com/todos"

async def get_tasks() -> Optional[List[Dict[str, Any]]]:
    logging.info("fetching all tasks rn...")
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(BASE_URL, timeout=5.0)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            logging.error(f"HTTP cooked: {e.response.status_code}")
        except httpx.RequestError as e:
            logging.error(f"network died: {e}")
        return None

async def get_task_by_id(task_id: int) -> Optional[Dict[str, Any]]:
    url = f"{BASE_URL}/{task_id}"
    logging.info(f"grabbin task #{task_id}...")
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, timeout=5.0)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                logging.warning(f"task {task_id} got ghosted (404)")
            else:
                logging.error(f"HTTP cooked: {e.response.status_code}")
        except httpx.RequestError as e:
            logging.error(f"network died: {e}")
        return None

async def create_task(title: str, user_id: int) -> Optional[Dict[str, Any]]:
    logging.info(f"spinnin up task: '{title}'")
    payload = {
        "title": title,
        "completed": False,
        "userId": user_id
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(BASE_URL, json=payload, timeout=5.0)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            logging.error(f"POST got cooked: {e.response.status_code}")
        except httpx.RequestError as e:
            logging.error(f"network died: {e}")
        return None