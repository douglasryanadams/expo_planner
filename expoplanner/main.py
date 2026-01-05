import sys
from contextlib import asynccontextmanager

from fastapi import FastAPI
from loguru import logger
from sqlmodel import SQLModel

from expoplanner.model import engine
from expoplanner.rest import conference, room, attendee, presenter, panel
from expoplanner.view.registration import registration


def configure_logging():
    logger.remove()
    logger.add(
        sys.stdout,
        format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green>  <level>{level: <8}</level> - <level>{message}</level>",
        level="INFO",
        colorize=True,
    )


@asynccontextmanager
async def lifespan(app: FastAPI):
    configure_logging()
    logger.info("Starting application")
    SQLModel.metadata.create_all(engine)
    logger.info("Database tables created")

    yield

    logger.info("Stopping application")


app = FastAPI(lifespan=lifespan)
app.include_router(conference.conference_api)
app.include_router(room.room_api)
app.include_router(attendee.attendee_api)
app.include_router(presenter.presenter_api)
app.include_router(panel.panel_api)
app.include_router(registration)


@app.get("/")
async def root():
    return {"message": "Hello World"}
