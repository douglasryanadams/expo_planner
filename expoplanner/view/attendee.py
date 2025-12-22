from fastapi import APIRouter
from loguru import logger
from sqlmodel import select, delete

from expoplanner.model import Attendee, AttendeeTable, AttendeeBase
from expoplanner.dependency import DBSession

attendee_api = APIRouter(prefix="/attendee")


@attendee_api.post("/")
def create_attendee(attendee: AttendeeBase, db: DBSession):
    attendee_table = AttendeeTable.model_validate(attendee)
    db.add(attendee_table)
    db.commit()
    db.refresh(attendee_table)
    return Attendee.model_validate(attendee_table)


@attendee_api.get("/")
def read_attendees(db: DBSession, offset: int = 0, limit: int = 100):
    logger.info("Reading list of attendees")
    return db.exec(select(AttendeeTable).offset(offset).limit(limit)).all()


@attendee_api.get("/{attendee_id}")
def read_attendee(attendee_id: int, db: DBSession):
    logger.info("Reading attendee", extra={"attendee_id": attendee_id})
    return db.get(AttendeeTable, attendee_id)


@attendee_api.delete("/{attendee_id}")
def delete_attendee(attendee_id: int, db: DBSession):
    db.exec(delete(AttendeeTable).where(AttendeeTable.id == attendee_id))
    db.commit()
    return {"message": "Attendee deleted"}
