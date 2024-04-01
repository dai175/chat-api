import jwt
from sqlalchemy.orm import Session

from app.core.env import ALGORITHM, SECRET_KEY
from app.crud import crud_user
from app.models import User


def decode_token_and_get_user(db: Session, token: str) -> User | None:
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    email = payload.get("sub")
    if not email:
        return None
    user = crud_user.get_by_email(db=db, email=email)
    if not user:
        return None
    return user
