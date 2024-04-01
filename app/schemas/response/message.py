from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class ReceiverBase(BaseModel):
    receiver_id: UUID = Field(Field(..., title="受信者ID", examples=["c19a6479-540e-4b34-a1cf-7f93b9a7e4c8"]))
    read_at: datetime | None = Field(None, title="閲覧時間", examples=["2024-03-29T17:42:05.214862"])


class MessageBase(BaseModel):
    id: UUID = Field(..., title="メッセージID", examples=["123e4567-e89b-12d3-a456-426614174000"])
    content: str = Field(..., title="メッセージ内容", examples=["テスト"])
    sender_id: UUID = Field(..., title="送信者ID", examples=["ba209999-0c6c-11d2-97cf-00c04f8eea45"])
    receivers: list[ReceiverBase] = Field(..., title="受信者一覧", examples=[])


class PostMessageRes(BaseModel):
    id: UUID = Field(..., title="メッセージID", examples=["123e4567-e89b-12d3-a456-426614174000"])
    content: str = Field(..., title="メッセージ内容", examples=["テスト"])
    sender_id: UUID = Field(..., title="送信者ID", examples=["ba209999-0c6c-11d2-97cf-00c04f8eea45"])
    receiver_ids: list[UUID] = Field(..., title="受信者ID一覧", examples=[["c19a6479-540e-4b34-a1cf-7f93b9a7e4c8"]])


class GetMessagesRes(BaseModel):
    messages: list[MessageBase] = Field(..., title="メッセージ一覧", examples=[])


class GetMessageRes(MessageBase):
    pass
