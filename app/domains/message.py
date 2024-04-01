from datetime import datetime
from typing import cast
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.messages import ErrorMessages
from app.crud import crud_message, crud_message_status, crud_user
from app.models import Message, MessageStatus, User
from app.schemas.request.message import PostMessageParams


class MessageDomain:
    def __init__(self, db: Session, user: User) -> None:
        self.__db = db
        self.__user = user

    def get_messages(self) -> list[Message]:
        messages = crud_message.get_by_user_id(db=self.__db, user_id=cast(UUID, self.__user.id))
        return messages

    def get_message(self, message_id: UUID) -> Message:
        message = crud_message.get_by_id_and_user_id(
            db=self.__db, message_id=message_id, user_id=cast(UUID, self.__user.id)
        )
        if not message:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ErrorMessages.MESSAGE_NOT_FOUND)
        return message

    def create_message(self, params: PostMessageParams) -> Message:
        self.__validate_receiver_ids(receiver_ids=params.receiver_ids)

        message_statuses = [
            MessageStatus(
                receiver_id=receiver_id,
                read_at=datetime.now() if params.is_read else None,
            )
            for receiver_id in params.receiver_ids
        ]
        message = Message(
            content=params.content,
            sender_id=self.__user.id,
            message_statuses=message_statuses,
        )
        created_message = crud_message.create_or_update(db=self.__db, model=message)
        return created_message

    def delete_message(self, message_id: UUID) -> None:
        message = crud_message.get_by_id_and_sender_id(
            db=self.__db, message_id=message_id, sender_id=cast(UUID, self.__user.id)
        )
        if not message:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ErrorMessages.MESSAGE_NOT_FOUND)
        deleted_at = datetime.now()
        message.deleted_at = deleted_at
        for message_status in message.message_statuses:
            message_status.deleted_at = deleted_at
        crud_message.create_or_update(db=self.__db, model=message)

    def set_message_as_read(self, message_id: UUID) -> None:
        message_status = crud_message_status.get_by_message_id_and_receiver_id(
            db=self.__db, message_id=message_id, receiver_id=cast(UUID, self.__user.id)
        )
        if not message_status:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ErrorMessages.MESSAGE_NOT_FOUND)
        message_status.read_at = datetime.now()
        crud_message_status.create_or_update(db=self.__db, model=message_status)

    def __validate_receiver_ids(self, receiver_ids: list[UUID]) -> None:
        receivers = crud_user.get_by_ids(db=self.__db, user_ids=receiver_ids)
        if len(receiver_ids) != len(receivers):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ErrorMessages.RECEIVER_NOT_FOUND)
