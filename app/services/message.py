from typing import cast
from uuid import UUID

from fastapi import Request
from sqlalchemy.orm import Session

from app.core.constants import INCOMING_MESSAGE_SUBJECT
from app.core.env import FROM_EMAIL
from app.crud import crud_user
from app.domains.message import MessageDomain
from app.models import User
from app.schemas.request.message import PostMessageParams
from app.schemas.response.message import GetMessageRes, GetMessagesRes, MessageBase, PostMessageRes, ReceiverBase
from app.services.mail import MailService
from app.services.notification import NotificationService
from app.views.templates_config import templates


class MessageService:
    def __init__(self, db: Session, user: User, request: Request | None = None) -> None:
        self.__db = db
        self.__user = user
        self.__request = request

    def get_messages(self) -> GetMessagesRes:
        messages = MessageDomain(db=self.__db, user=self.__user).get_messages()
        response = GetMessagesRes(
            messages=[
                MessageBase(
                    id=cast(UUID, message.id),
                    content=message.content,
                    sender_id=cast(UUID, message.sender_id),
                    receivers=[
                        ReceiverBase(
                            receiver_id=status.receiver_id,
                            read_at=status.read_at,
                        )
                        for status in message.message_statuses
                    ],
                )
                for message in messages
            ],
        )

        return response

    def get_message(self, message_id: UUID) -> GetMessageRes:
        message = MessageDomain(db=self.__db, user=self.__user).get_message(message_id=message_id)
        response = GetMessageRes(
            id=cast(UUID, message.id),
            content=message.content,
            sender_id=cast(UUID, message.sender_id),
            receivers=[
                ReceiverBase(
                    receiver_id=status.receiver_id,
                    read_at=status.read_at,
                )
                for status in message.message_statuses
            ],
        )

        return response

    async def create_message(self, params: PostMessageParams) -> PostMessageRes:
        created_message = MessageDomain(self.__db, user=self.__user).create_message(params=params)
        response = PostMessageRes(
            id=cast(UUID, created_message.id),
            content=created_message.content,
            sender_id=cast(UUID, created_message.sender_id),
            receiver_ids=[status.receiver_id for status in created_message.message_statuses],
        )
        await self.__send_incoming_message(receiver_ids=params.receiver_ids)
        return response

    def delete_message(self, message_id: UUID) -> None:
        MessageDomain(db=self.__db, user=self.__user).delete_message(message_id=message_id)

    def set_message_as_read(self, message_id: UUID) -> None:
        MessageDomain(db=self.__db, user=self.__user).set_message_as_read(message_id=message_id)

    async def __send_incoming_message(self, receiver_ids: list[UUID]) -> None:
        mail_service = MailService()
        notification_service = NotificationService()
        receivers = crud_user.get_by_ids(db=self.__db, user_ids=receiver_ids)
        for receiver in receivers:
            if not receiver.notification_setting:
                continue

            template_response = templates.TemplateResponse(
                "incoming_message.txt",
                {"request": self.__request, "name": receiver.email},
            )
            body = template_response.body.decode("utf-8")
            if receiver.notification_setting.is_email_notification:
                await mail_service.send_mail(
                    subject=INCOMING_MESSAGE_SUBJECT,
                    body=body,
                    from_email=FROM_EMAIL,
                    to_email=receiver.email,
                )
            elif receiver.notification_setting.is_push_notification:
                await notification_service.push_notifications(
                    title=INCOMING_MESSAGE_SUBJECT,
                    receiver_id_str=str(cast(UUID, receiver.id)),
                    body=body,
                )
