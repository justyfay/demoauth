from users.repository import UsersRepository
from users.schemas import UserSchema


async def get_user_db(username: str) -> UserSchema:
    return await UsersRepository.find_one_or_none(email=username)
