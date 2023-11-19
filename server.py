import base64
import hmac
import hashlib
import json

from typing import Optional
from fastapi import FastAPI, Cookie, Body
from fastapi.responses import Response

app = FastAPI()

SECRET_KEY = "99b4aef3cd966fda701668e41ab8622de476ae2a544ac31e8e22cb22008ba8a4"
PASSWORD_SALT = "dcd3fd3c419643e56999df7ba5969177301a440fbaa3c67902a9892b48897496"


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


users = {
    "alexy@user.com": {
        "name": "Алексей",
        "password": "2ff611f748e3b3bbf3750d0cee3a5b8fc6d0dfb4fc474f68a68915c2b064ee1d",
        "balance": 100_000
    },
    "petr@user.com": {
        "name": "Петр",
        "password": "767f7d1dff4536986fed335aea0d6a1af0cb9b042355408ab1c1a684cb7f2d5f",
        "balance": 555_555
    }

}


def verify_password(username: str, password: str) -> bool:
    password_hash = hashlib.sha256((password + PASSWORD_SALT).encode()).hexdigest().lower()
    stored_password_hash = users[username]["password"].lower()
    return password_hash == stored_password_hash


@app.get("/")
def index_page(username: Optional[str] = Cookie(default=None)) -> Response:
    with open("templates/login.html", "r") as f:
        login_page = f.read()
    if not username:
        return Response(login_page, media_type="text/html")
    valid_username = get_username_from_signed_string(username)
    if not valid_username:
        response = Response(login_page, media_type="text/html")
        response.delete_cookie(key="username")
        return response
    try:
        user = users[valid_username]
    except KeyError:
        response = Response(login_page, media_type="text/html")
        response.delete_cookie(key="username")
        return response
    return Response(F"Привет, {users[valid_username]['name']}!", media_type="text/html")


@app.post("/login")
def process_login_page(data=Body(...)):
    data_decoded = json.loads(json.dumps(data))
    username = data_decoded["username"]
    password = data_decoded["password"]
    user = users.get(username)
    if not user or not verify_password(username, password):
        return Response(
            json.dumps({
                "success": False,
                "message": "Я вас не знаю!"
            }),
            media_type="application/json"
        )
    response = Response(
        json.dumps({
            "success": True,
            "message": F"Привет, {user['name']}!<br />Баланс: {user['balance']}",
        }),
        media_type="application/json"
    )
    username_signed = base64.b64encode(username.encode()).decode() + "." + sign_data(username)
    response.set_cookie(key="username", value=username_signed)
    return response
