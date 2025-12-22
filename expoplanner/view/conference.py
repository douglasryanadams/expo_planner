from fastapi import APIRouter
from loguru import logger
from sqlmodel import select, delete

from expoplanner.model import Conference, ConferenceTable, ConferenceBase
from expoplanner.dependency import DBSession

conference_api = APIRouter(prefix="/conference")


@conference_api.post("/")
def create_conference(conference: ConferenceBase, db: DBSession):
    conference_table = ConferenceTable.model_validate(conference)
    db.add(conference_table)
    db.commit()
    db.refresh(conference_table)
    return Conference.model_validate(conference_table)


@conference_api.get("/")
def read_conferences(db: DBSession, offset: int = 0, limit: int = 100):
    logger.info("Reading list of conferences")
    return db.exec(select(ConferenceTable).offset(offset).limit(limit)).all()


@conference_api.get("/{conference_id}")
def read_conference(conference_id: int, db: DBSession):
    logger.info("Reading conference", extra={"conference_id": conference_id})
    return db.get(ConferenceTable, conference_id)


@conference_api.delete("/{conference_id}")
def delete_conference(conference_id: int, db: DBSession):
    db.exec(delete(ConferenceTable).where(ConferenceTable.id == conference_id))
    db.commit()
    return {"message": "Conference deleted"}
