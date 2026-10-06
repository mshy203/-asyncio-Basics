from typing import Optional 
from pydantic import BaseModel, Field
# req model
class TaskCreate(BaseModel):
 title: str = Field(..., min_length=1, max_length=100, description="title")
 description: Optional[str] = Field(None, max_length=500, description="desc")
 priority: int = Field(1, ge=1, le=4, description="priority")

class TaskUpdate(BaseModel):
 title: Optional[str] = Field(None, min_length=1, max_length=100)
 description: Optional[str] = Field(None, max_length=500)
 priority: Optional[int] = Field(None, ge=1, le=4)
 status: Optional[str] = Field(None, description="status")

class TaskResponse(BaseModel):
 id: int
 title: str
 description: Optional[str] = None
 priority: int
 status: str
 xp: int

class Config:
 from_attributes = True

fake_db = []
id_counter = 1