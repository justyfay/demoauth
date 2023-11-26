import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY: str = os.getenv("SECRET_KEY")
PASSWORD_SALT: str = os.getenv("PASSWORD_SALT")
SQLITE_URL: str = os.getenv("SQLITE_URL")
