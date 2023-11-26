from typing import Optional

from fastapi import APIRouter, Cookie
from starlette.responses import Response

from auth.auth import get_username_from_signed_string
from users.schemas import UserSchema
from users.utils import get_user_db

router = APIRouter(
    prefix="",
    tags=["Страницы"],
)


@router.get("/")
async def index_page(username: Optional[str] = Cookie(default=None)) -> Response:
    with open("templates/login.html", "r") as f:
        login_page: str = f.read()
    if not username:
        return Response(login_page, media_type="text/html")
    valid_username: str = get_username_from_signed_string(username)
    if not valid_username:
        response: Response = Response(login_page, media_type="text/html")
        response.delete_cookie(key="username")
        return response
    try:
        actual_user: UserSchema = await get_user_db(username=valid_username)
    except KeyError:
        response: Response = Response(login_page, media_type="text/html")
        response.delete_cookie(key="username")
        return response
    return Response(F"Здравствуйте, {actual_user.name}! Вы были авторизованы ранее.", media_type="text/html")
