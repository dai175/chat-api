from pydantic import BaseModel, Field


class RegisterParams(BaseModel):
    email: str = Field(..., title="メールアドレス", description="登録するユーザーのメールアドレス")
    password: str = Field(..., title="パスワード", description="登録するユーザーのパスワード")
