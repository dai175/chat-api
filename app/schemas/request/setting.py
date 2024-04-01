from fastapi import HTTPException, status
from pydantic import BaseModel, Field, field_validator

from app.core.messages import ErrorMessages


class PostSettingParams(BaseModel):
    notification_method: int = Field(..., title="通知手段", description="登録する通知手段")

    @field_validator("notification_method")
    def validate_notification_method(cls, v: int) -> int:
        if v not in [0, 1, 2]:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=ErrorMessages.INVALID_NOTIFICATION_METHOD
            )
        return v
