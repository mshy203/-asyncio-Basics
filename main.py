import asyncio
import time

async def fetch_data(name, delay):
    print(f"-> Запит до {name} розпочато")
    await asyncio.sleep(delay) 
    print(f" Запит до {name} завершено")
    return f"Дані з {name}"
async def main():
 start_time = time.time()
 print("Головна програма стартувала.")
 result1, result2 = await asyncio.gather(
  fetch_data("Бази даних", 2),
  fetch_data("API погоди", 1)
 )
 print(f"Отримано результати: {result1}, {result2}")
 end_time = time.time()
 print(f"Загальний час виконання: {end_time - start_time:.2f} секунд")
asyncio.run(main())