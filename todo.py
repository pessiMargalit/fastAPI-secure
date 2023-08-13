import uuid
from collections import defaultdict
from typing import Optional

from pydantic import BaseModel, Field


class Todo(BaseModel):
    id: int = Field(default_factory=lambda: uuid.uuid4().int)
    title: str
    description: Optional[str] = None
    owner: str
    completed: bool = False


class TodoContent(BaseModel):
    title: str
    description: Optional[str] = None
    completed: Optional[bool] = False


todo_dict = defaultdict(dict)

