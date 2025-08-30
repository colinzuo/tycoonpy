from __future__ import annotations

import logging
from typing import TYPE_CHECKING, cast

from sqlmodel import SQLModel, create_engine, text

if TYPE_CHECKING:
    from sqlalchemy import Engine

mod_logger = logging.getLogger(__name__)

engine: Engine = cast("Engine", None)

def get_engine() -> Engine:
    return engine

def setup_database(db_url: str) -> None:
    global engine

    mod_logger.info(f"db_url {db_url}")

    if db_url.startswith("sqlite"):
        connect_args = {"check_same_thread": False}
        engine = create_engine(db_url, echo=False, connect_args=connect_args)
        with engine.connect() as connection:
            connection.execute(text("PRAGMA foreign_keys=ON"))

    SQLModel.metadata.create_all(engine)
