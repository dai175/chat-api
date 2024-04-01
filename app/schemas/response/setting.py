from uuid import UUID

from pydantic import BaseModel, Field


class PostSettingRes(BaseModel):
    id: UUID = Field(Field(..., title="通知設定ID", examples=["ba209999-0c6c-11d2-97cf-00c04f8eea45"]))
    notification_method: int | None = Field(None, title="通知手段", examples=[1])
