import asyncio
import time

async def get_data(name, delay):
    print("Typeshi")
    await asyncio.sleep(delay)
    print("Typeshi2")
    return

async def main():
    start_time = time.time()

    result1, result2 = await asyncio.gather(
     get_data("Lol", 1)
     get_data("Lmao", 3)
     )
    print("Lol2a")
    end_time = time.time()