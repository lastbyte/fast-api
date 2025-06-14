from datetime import datetime
from sqlmodel import Field, SQLModel
from pydantic import ConfigDict, field_serializer
from typing import Any, Dict


class BaseModel(SQLModel, table=False):
    
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime = Field(default=None, nullable=False)
    updated_at: datetime = Field(default=datetime.now(), nullable=False)

    def model_dump(self, **kwargs) -> Dict[str, Any]:
        # Default exclude relationships unless explicitly included
        if 'exclude' not in kwargs:
            kwargs['exclude'] = set()
        if isinstance(kwargs['exclude'], set):
            kwargs['exclude'].add('users')
        return super().model_dump(**kwargs)

    @field_serializer('created_at', 'updated_at')
    def serialize_datetime(self, dt: datetime | None) -> str | None:
        return dt.isoformat() if dt else None


class BaseEntity(BaseModel, table=False):
    create_by: int = Field(nullable=False)