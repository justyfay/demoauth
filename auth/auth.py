import base64
import hashlib
import hmac
from typing import Optional

from env import SECRET_KEY, PASSWORD_SALT
from users.schemas import UserSchema
from users.utils import get_user_db


def sign_data(data: str) -> str:
    return hmac.new(
        SECRET_KEY.encode(),
        msg=data.encode(),
        digestmod=hashlib.sha256
    ).hexdigest().upper()


def get_username_from_signed_string(username_signed: str) -> Optional[str]:
    username_base64, sign = username_signed.split(".")
    username = base64.b64decode(username_base64.encode()).decode()
    valid_sign = sign_data(username)
    if hmac.compare_digest(valid_sign, sign):
        return username


async def verify_password(username: str, password: str) -> bool:
    password_hash: str = hashlib.sha256((password + PASSWORD_SALT).encode()).hexdigest().lower()
    searched_user: UserSchema = await get_user_db(username=username)
    stored_password_hash: str = searched_user.password.lower()
    return password_hash == stored_password_hash
