from typing import cast
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session, joinedload

from app.core.messages import ErrorMessages
from app.models import User


def get_by_id(db: Session, user_id: UUID) -> User | None:
    return (
        db.query(User)
        .filter(
            User.id == user_id,
            User.deleted_at.is_(None),
        )
        .one_or_none()
    )


def get_by_ids(db: Session, user_ids: list[UUID]) -> list[User]:
    return cast(
        list[User],
        db.query(User)
        .options(joinedload(User.notification_setting))
        .filter(
            User.id.in_(user_ids),
            User.deleted_at.is_(None),
        )
        .all(),
    )


def get_by_email(db: Session, email: str) -> User | None:
    return (
        db.query(User)
        .filter(
            User.email == email,
            User.deleted_at.is_(None),
        )
        .one_or_none()
    )


def create_or_update(db: Session, model: User) -> User:
    try:
        db.add(model)
        db.commit()
    except Exception:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=ErrorMessages.MODEL_SAVE_FAILED)
    return model
