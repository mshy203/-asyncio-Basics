from typing import Optional 
from pydantic import BaseModel, Field

class CreateTask(BaseModel):
    title: str = Field(..., min_lenght = 10, max_lenght = 100, description="Title")
    desc: str = Optional[str] = Field(None, max_lenght = 500)
    priority: int = Field(1, ge=1, le=5, description="Priority to 5")
    