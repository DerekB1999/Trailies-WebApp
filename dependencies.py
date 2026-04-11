from typing import Optional
from fastapi import Cookie, Depends
from models import User
from security import verify_access_token
from database import get_session
from sqlmodel import select, Session


async def get_current_user(
    access_token: str = Cookie(None),
    session: Session = Depends(get_session),
) -> Optional[User]:
    if not access_token:
        return None

    # Verify and decode JWT
    payload = verify_access_token(access_token)
    if payload is None:
        return None

    # Extract subject from payload
    username: str | None = payload.get('sub')
    if username is None:
        return None

    # Look up user in DB
    query = select(User).where(User.username == username)
    user = session.exec(query).first()

    return user
