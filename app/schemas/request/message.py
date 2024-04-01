from uuid import UUID

from pydantic import BaseModel, Field


class PostMessageParams(BaseModel):
    content: str = Field(..., title="メッセージ内容", description="登録するメッセージの内容")
    receiver_ids: list[UUID] = Field(..., title="受信者ID一覧", description="登録するメッセージの受信者ID一覧")
    is_read: bool = Field(False, title="既読", description="登録するメッセージが既読かどうか")
