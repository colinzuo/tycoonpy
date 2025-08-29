from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from sqlmodel import SQLModel, create_engine, text

if TYPE_CHECKING:
    from sqlalchemy import Engine

mod_logger = logging.getLogger(__name__)

engine: Engine

def setup_database(db_url: str) -> None:
    global engine

    mod_logger.info(f"db_url {db_url}")

    if db_url.startswith("sqlite"):
        connect_args = {"check_same_thread": False}
        engine = create_engine(db_url, echo=True, connect_args=connect_args)
        with engine.connect() as connection:
            connection.execute(text("PRAGMA foreign_keys=ON"))

    SQLModel.metadata.create_all(engine)
