from loguru import logger
import subprocess
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI

from auth.router import router as users_router
from pages.router import router as pages_router
from database import create_tables, delete_tables


@asynccontextmanager
async def lifespan(app: FastAPI):  # noqa
    await create_tables()
    logger.info("Create Database")
    db_name: Path = Path('demo-auth.db').resolve()
    csv_file: Path = Path('users.csv').resolve()
    result: subprocess.CompletedProcess[bytes] = subprocess.run(
        ['sqlite3',
         str(db_name),
         '-cmd',
         '.mode csv',
         '.import --skip 1 ' + str(csv_file).replace('\\', '\\\\')
         + ' users'],
        capture_output=True)
    logger.info("Imported CSV database dump.")
    yield
    await delete_tables()
    logger.info("Delete Database")


app: FastAPI = FastAPI(lifespan=lifespan)
app.include_router(users_router)
app.include_router(pages_router)
