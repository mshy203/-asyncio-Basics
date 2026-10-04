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