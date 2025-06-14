from datetime import datetime
from sqlmodel import Field, SQLModel
from pydantic import ConfigDict, field_serializer


class BaseModel(SQLModel, table=False):
    model_config = ConfigDict(
        arbitrary_types_allowed=True
    )
    
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime = Field(default=None, nullable=False)
    updated_at: datetime = Field(default=datetime.now(), nullable=False)

    @field_serializer('created_at', 'updated_at')
    def serialize_datetime(self, dt: datetime | None) -> float | None:
        return dt.timestamp() if dt else None


class BaseEntity(BaseModel, table=False):
    create_by: int = Field(nullable=False)