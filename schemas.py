from datetime import datetime
from pydantic import BaseModel, Field


# ----- Thread -----

class ThreadCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    created_by: str = Field(..., min_length=1, max_length=64)
    display_name: str | None = Field(None, max_length=64)


class ThreadResponse(BaseModel):
    id: int
    title: str
    created_by: str
    display_name: str | None
    created_at: datetime
    post_count: int

    model_config = {"from_attributes": True}


# ----- Post -----

class PostCreate(BaseModel):
    body: str = Field(..., min_length=1)
    created_by: str = Field(..., min_length=1, max_length=64)
    display_name: str | None = Field(None, max_length=64)


class PostResponse(BaseModel):
    id: int
    thread_id: int
    body: str
    created_by: str
    display_name: str | None
    created_at: datetime

    model_config = {"from_attributes": True}
