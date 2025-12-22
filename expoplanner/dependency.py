from typing import Annotated

from fastapi import Depends
from sqlmodel import Session

from expoplanner.model import engine


def get_session():
    with Session(engine) as session:
        yield session


DBSession = Annotated[Session, Depends(get_session)]
