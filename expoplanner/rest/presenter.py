from fastapi import APIRouter
from loguru import logger
from sqlmodel import select, delete

from expoplanner.model import Presenter, PresenterTable, PresenterBase
from expoplanner.dependency import DBSession

presenter_api = APIRouter(prefix="/rest/presenter")


@presenter_api.post("/")
def create_presenter(presenter: PresenterBase, db: DBSession):
    presenter_table = PresenterTable.model_validate(presenter)
    db.add(presenter_table)
    db.commit()
    db.refresh(presenter_table)
    return Presenter.model_validate(presenter_table)


@presenter_api.get("/")
def read_presenters(db: DBSession, offset: int = 0, limit: int = 100):
    logger.info("Reading list of presenters")
    return db.exec(select(PresenterTable).offset(offset).limit(limit)).all()


@presenter_api.get("/{presenter_id}")
def read_presenter(presenter_id: int, db: DBSession):
    logger.info("Reading presenter", extra={"presenter_id": presenter_id})
    return db.get(PresenterTable, presenter_id)


@presenter_api.delete("/{presenter_id}")
def delete_presenter(presenter_id: int, db: DBSession):
    db.exec(delete(PresenterTable).where(PresenterTable.id == presenter_id))
    db.commit()
    return {"message": "Presenter deleted"}
