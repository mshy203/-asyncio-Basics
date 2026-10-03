import asyncio
import logging
from typing import Any, Dict, List, Optional

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

BASE_URL: str = "https://jsonplaceholder.typicode.com/todos"

