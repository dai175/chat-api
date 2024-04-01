from datetime import datetime
from uuid import uuid4

from sqlalchemy import TIMESTAMP, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.db import Base
from app.models.mixins import TimestampMixin


class MessageStatus(Base, TimestampMixin):
    __tablename__ = "message_statuses"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4, comment="ID")
    message_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("messages.id"), nullable=False, comment="メッセージID"
    )
    receiver_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, comment="受信者ID"
    )
    read_at: Mapped[datetime | None] = mapped_column(TIMESTAMP, nullable=True, default=None, comment="閲覧時間")

    message = relationship("Message", back_populates="message_statuses")
    receiver = relationship("User", back_populates="message_statuses")
