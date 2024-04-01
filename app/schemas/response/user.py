from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class RegisterRes(BaseModel):
    id: UUID = Field(Field(..., title="ユーザーID", examples=["ba209999-0c6c-11d2-97cf-00c04f8eea45"]))
    email: str = Field(Field(..., title="メールアドレス", examples=["test@example.com"]))
    created_at: datetime = Field(..., title="作成時間", examples=["2024-03-29T17:42:05.214862"])
    updated_at: datetime = Field(..., title="更新時間", examples=["2024-03-29T17:42:05.214862"])


class TokenRes(BaseModel):
    access_token: str = Field(Field(..., title="トークン", examples=[""]))
    token_type: str = Field(Field(..., title="トークンタイプ", examples=["bearer"]))
