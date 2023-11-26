import base64
import json

from fastapi import APIRouter, Body
from starlette.responses import Response

from auth.auth import verify_password, get_user_db, sign_data
from users.schemas import UserSchema, UserLoginSchema

router = APIRouter(
    prefix="",
    tags=["Авторизация"],
)


@router.post("/login")
async def process_login_page(data=Body(...)):
    data_decoded: dict = json.loads(json.dumps(data))
    username: str = data_decoded["username"]
    password: str = data_decoded["password"]
    user: UserSchema = await get_user_db(username=username)
    checked_password = await verify_password(username, password)
    if not user or not checked_password:
        return UserLoginSchema().model_dump()
    response: Response = Response(
        content=UserLoginSchema.model_construct(
            success=True,
            message=f"Добро пожаловать, {user.name}!"
        ).model_dump_json(), media_type="application/json")
    username_signed: str = base64.b64encode(username.encode()).decode() + "." + sign_data(username)
    response.set_cookie(key="username", value=username_signed, httponly=True, expires=3600)
    return response
