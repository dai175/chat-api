from enum import Enum
from uuid import uuid4

from sqlalchemy import ForeignKey, SmallInteger
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.db import Base
from app.models.mixins import TimestampMixin


class NotificationMethod(Enum):
    NONE = 0
    EMAIL = 1
    PUSH = 2


class NotificationSetting(Base, TimestampMixin):
    __tablename__ = "notification_settings"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4, comment="ID")
    user_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, comment="ユーザーID"
    )
    method: Mapped[int] = mapped_column(SmallInteger, nullable=True, default=0, comment="通知手段")

    user = relationship("User", back_populates="notification_setting")

    @hybrid_property
    def is_email_notification(self) -> bool:
        return self.method == NotificationMethod.EMAIL.value

    @hybrid_property
    def is_push_notification(self) -> bool:
        return self.method == NotificationMethod.PUSH.value
