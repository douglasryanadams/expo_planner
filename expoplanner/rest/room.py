from fastapi import APIRouter
from loguru import logger
from sqlmodel import select, delete

from expoplanner.model import Room, RoomTable, RoomBase
from expoplanner.dependency import DBSession

room_api = APIRouter(prefix="/rest/room")


@room_api.post("/")
def create_room(room: RoomBase, db: DBSession):
    room_table = RoomTable.model_validate(room)
    db.add(room_table)
    db.commit()
    db.refresh(room_table)
    return Room.model_validate(room_table)


@room_api.get("/")
def read_rooms(db: DBSession, offset: int = 0, limit: int = 100):
    logger.info("Reading list of rooms")
    return db.exec(select(RoomTable).offset(offset).limit(limit)).all()


@room_api.get("/{room_id}")
def read_room(room_id: int, db: DBSession):
    logger.info("Reading room", extra={"room_id": room_id})
    return db.get(RoomTable, room_id)


@room_api.delete("/{room_id}")
def delete_room(room_id: int, db: DBSession):
    db.exec(delete(RoomTable).where(RoomTable.id == room_id))
    db.commit()
    return {"message": "Room deleted"}
