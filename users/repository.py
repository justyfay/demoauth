from typing import Tuple, Any, Optional, Type

from loguru import logger
from sqlalchemy import select, Select, Result, RowMapping

from database import new_session, Base, UsersModel
from users.schemas import UserSchema


class UsersRepository:
    model: Type[Base] = UsersModel
    @classmethod
    async def find_one_or_none(cls, **filter_by) -> Optional[UserSchema]:
        async with new_session() as session:
            query: Select[Tuple | Any] = select(cls.model.__table__.columns).filter_by(**filter_by)
            logger.debug(f"Query: {query}")
            query_execute: Result[Tuple | Any] = await session.execute(query)
            result: Optional[RowMapping] = query_execute.mappings().one_or_none()
            logger.debug(f"Result: {result}")
            return result
