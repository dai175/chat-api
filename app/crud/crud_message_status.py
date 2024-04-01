from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.messages import ErrorMessages
from app.models import MessageStatus


def get_by_message_id_and_receiver_id(db: Session, message_id: UUID, receiver_id: UUID) -> MessageStatus | None:
    return (
        db.query(MessageStatus)
        .filter(
            MessageStatus.message_id == message_id,
            MessageStatus.receiver_id == receiver_id,
            MessageStatus.deleted_at.is_(None),
        )
        .one_or_none()
    )


def create_or_update(db: Session, model: MessageStatus) -> MessageStatus:
    try:
        db.add(model)
        db.commit()
    except Exception:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=ErrorMessages.MODEL_SAVE_FAILED)
    return model
