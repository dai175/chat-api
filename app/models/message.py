from uuid import uuid4

from sqlalchemy import ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.db import Base
from app.models.mixins import TimestampMixin


class Message(Base, TimestampMixin):
    __tablename__ = "messages"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4, comment="ID")
    content: Mapped[str] = mapped_column(Text, nullable=False, comment="内容")
    sender_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, comment="送信者ID"
    )

    message_statuses = relationship("MessageStatus", back_populates="message")
    sender = relationship("User", back_populates="messages")
