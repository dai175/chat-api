from uuid import uuid4

from sqlalchemy import String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.db import Base
from app.models.mixins import TimestampMixin


class User(Base, TimestampMixin):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4, comment="ID")
    email: Mapped[str] = mapped_column(String(320), nullable=False, unique=True, comment="メールアドレス")
    hashed_password: Mapped[str] = mapped_column(Text, nullable=False, comment="パスワードハッシュ")

    notification_setting = relationship("NotificationSetting", uselist=False, back_populates="user")
    messages = relationship("Message", back_populates="sender")
    message_statuses = relationship("MessageStatus", back_populates="receiver")
