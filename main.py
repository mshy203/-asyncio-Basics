Ось код без жодних коментарів:

Python
import asyncio
import logging
import httpx

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

async def fetch_user_data(user_id: int):
    url = f"https://jsonplaceholder.typicode.com/users/{user_id}"
    logging.info(f"Надсилаємо GET-запит на {url}")

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, timeout=5.0)
            logging.info(f"Отримано статус код: {response.status_code}")
            response.raise_for_status()
            data = response.json()
            logging.info("JSON в пайтоні")
            return data
        #Written by AI below, error logging 
        except httpx.HTTPStatusError as e:
            logging.error(f"HTTP помилка! Статус: {e.response.status_code} для URL: {url}")
        except httpx.RequestError as e:
            logging.error(f"Помилка мережі (можливо, немає інтернету або таймаут): {e}")
        except Exception as e:
            logging.error(f"Непередбачувана помилка: {e}")
        return None

    async def main():
     print("--- ТЕСТ 1: Успішний запит ---")
     user_data = await fetch_user_data(1)
     if user_data:
        print(f"Результат Python: Ім'я — {user_data.get('name')}, Місто — {user_data.get('address', {}).get('city')}")

     print("\n--- ТЕСТ 2: Помилковий запит (404) ---")
     await fetch_user_data(9999)

asyncio.run(main())