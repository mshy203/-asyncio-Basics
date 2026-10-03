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

async def create_task(title: str, user_id: int) -> Optional[Dict[str, Any]]:
    logging.info(f"Створення нової задачі: '{title}'")
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
            logging.error(f"Не вдалося створити задачу. Статус: {e.response.status_code}")
        except httpx.RequestError as e:
            logging.error(f"Помилка мережі: {e}")
        return None

async def main() -> None:
    print("=" * 40)
    print("1. ТЕСТ: Отримання однієї задачі")
    print("=" * 40)
    task = await get_task_by_id(1)
    if task:
        print(f"ID: {task.get('id')}")
        print(f"Заголовок: {task.get('title')}")
        print(f"Виконано: {'✅ Так' if task.get('completed') else '❌ Ні'}\n")

    print("=" * 40)
    print("2. ТЕСТ: Створення нової задачі (POST)")
    print("=" * 40)
    new_task = await create_task(title="Вивчити Async Python та Type Hints", user_id=1)
    if new_task:
        print(f"Створено з ID: {new_task.get('id')}")
        print(f"Назва: {new_task.get('title')}")
        print(f"Користувач ID: {new_task.get('userId')}\n")

    print("=" * 40)
    print("3. ТЕСТ: Обробка помилки 404")
    print("=" * 40)
    await get_task_by_id(99999)

    print("=" * 40)
    print("4. ТЕСТ: Отримання списку задач (перші 3 шт.)")
    print("=" * 40)
    tasks = await get_tasks()
    if tasks:
        for t in tasks[:3]:
            status = "✅" if t.get('completed') else "❌"
            print(f"[{status}] #{t.get('id')} — {t.get('title')}")

asyncio.run(main())