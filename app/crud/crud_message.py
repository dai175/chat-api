from typing import cast
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.core.messages import ErrorMessages
from app.models import Message, MessageStatus


def get_by_id_and_sender_id(db: Session, message_id: UUID, sender_id: UUID) -> Message | None:
    return (
        db.query(Message)
        .filter(
            Message.id == message_id,
            Message.sender_id == sender_id,
            Message.deleted_at.is_(None),
        )
        .one_or_none()
    )


def get_by_id_and_receiver_id(db: Session, message_id: UUID, receiver_id: UUID) -> list[Message]:
    return cast(
        list[Message],
        db.query(Message)
        .join(MessageStatus, Message.id == MessageStatus.message_id)
        .filter(
            Message.id == message_id,
            MessageStatus.receiver_id == receiver_id,
            Message.deleted_at.is_(None),
        )
        .all(),
    )


def get_by_id_and_user_id(db: Session, message_id: UUID, user_id: UUID) -> Message | None:
    return (
        db.query(Message)
        .join(MessageStatus, Message.id == MessageStatus.message_id)
        .filter(
            Message.id == message_id,
            Message.deleted_at.is_(None),
            or_(
                Message.sender_id == user_id,
                MessageStatus.receiver_id == user_id,
            ),
        )
        .one_or_none()
    )


def get_by_user_id(db: Session, user_id: UUID) -> list[Message]:
    return cast(
        list[Message],
        db.query(Message)
        .join(MessageStatus, Message.id == MessageStatus.message_id)
        .filter(
            Message.deleted_at.is_(None),
            or_(
                Message.sender_id == user_id,
                MessageStatus.receiver_id == user_id,
            ),
        )
        .all(),
    )


def create_or_update(db: Session, model: Message) -> Message:
    try:
        db.add(model)
        db.commit()
    except Exception:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=ErrorMessages.MODEL_SAVE_FAILED)
    return model
