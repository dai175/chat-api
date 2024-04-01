from datetime import datetime

from sqlalchemy import TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP,
        nullable=False,
        default=datetime.now(),
        comment="作成時間",
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP,
        nullable=False,
        default=datetime.now(),
        onupdate=datetime.now(),
        comment="更新時間",
    )
    deleted_at: Mapped[datetime | None] = mapped_column(
        TIMESTAMP,
        nullable=True,
        default=None,
        comment="削除時間",
    )
