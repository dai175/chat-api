from pusher_push_notifications import PushNotifications

from app.core.env import PUSHER_INSTANCE_ID, PUSHER_SECRET_KEY


class NotificationService:
    def __init__(self, instance_id: str = PUSHER_INSTANCE_ID, secret_key: str = PUSHER_SECRET_KEY):
        self.__beams_client = PushNotifications(
            instance_id=instance_id,
            secret_key=secret_key,
        )

    async def push_notifications(self, title: str, body: str, receiver_id_str: str):
        response = self.__beams_client.publish_to_interests(
            interests=[receiver_id_str],
            publish_body={
                "web": {
                    "notification": {
                        "title": title,
                        "body": body,
                    }
                }
            },
        )
        return response
