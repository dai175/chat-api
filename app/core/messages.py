from pydantic import BaseModel


class ErrorMessages:
    MESSAGE_NOT_FOUND = "メッセージが見つかりませんでした"
    MODEL_SAVE_FAILED = "更新できませんでした"
    RECEIVER_NOT_FOUND = "受信者が見つかりませんでした"
    LOGIN_FAILED = "ログインできませんでした"
    INVALID_NOTIFICATION_METHOD = "通知手段が正しくありません"
    INVALID_TOKEN = "認証トークンが無効です"


class WebSocketError(BaseModel):
    code: int
    reason: str


class WebsocketErrorMessages:
    INVALID_RECEIVER = WebSocketError(code=4000, reason="受信者が見つかりませんでした")
