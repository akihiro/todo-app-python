from contextlib import asynccontextmanager
from fastapi import FastAPI
from typing import Optional
from sqlmodel import Field
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker

from .settings import settings


engine = create_async_engine(settings.DSN, echo=True)
async_session = async_sessionmaker(engine, expire_on_commit=False)


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    yield
    await engine.dispose()


class Item(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    counter: int = None
