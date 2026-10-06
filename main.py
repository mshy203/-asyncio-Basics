from typing import Optional 
from pydantic import BaseModel, Field
# req model
class TaskCreate(BaseModel):
 title: str = Field(..., min_length=1, max_length=100, description="title")
 description: Optional[str] = Field(None, max_length=500, description="desc")
 priority: int = Field(1, ge=1, le=4, description="priority")

