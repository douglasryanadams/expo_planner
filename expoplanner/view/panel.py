from fastapi import APIRouter
from loguru import logger
from sqlmodel import select, delete

from expoplanner.model import Panel, PanelTable, PanelBase
from expoplanner.dependency import DBSession

panel_api = APIRouter(prefix="/panel")


@panel_api.post("/")
def create_panel(panel: PanelBase, db: DBSession):
    panel_table = PanelTable.model_validate(panel)
    db.add(panel_table)
    db.commit()
    db.refresh(panel_table)
    return Panel.model_validate(panel_table)


@panel_api.get("/")
def read_panels(db: DBSession, offset: int = 0, limit: int = 100):
    logger.info("Reading list of panels")
    return db.exec(select(PanelTable).offset(offset).limit(limit)).all()


@panel_api.get("/{panel_id}")
def read_panel(panel_id: int, db: DBSession):
    logger.info("Reading panel", extra={"panel_id": panel_id})
    return db.get(PanelTable, panel_id)


@panel_api.delete("/{panel_id}")
def delete_panel(panel_id: int, db: DBSession):
    db.exec(delete(PanelTable).where(PanelTable.id == panel_id))
    db.commit()
    return {"message": "Panel deleted"}
