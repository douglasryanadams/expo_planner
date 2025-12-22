from datetime import date, datetime

from sqlmodel import SQLModel, Field, create_engine

engine = create_engine("sqlite:///tmp.db", connect_args={"check_same_thread": False})


class ConferenceBase(SQLModel):
    name: str = Field(index=True)
    location: str
    start_date: date
    end_date: date


class ConferenceTable(ConferenceBase, table=True):
    __tablename__ = "conference"
    id: int | None = Field(default=None, primary_key=True)


class Conference(ConferenceBase):
    id: int


class RoomBase(SQLModel):
    label: str = Field(index=True)
    location: str
    capacity: int
    conference: int = Field(foreign_key="conference.id")


class RoomTable(RoomBase, table=True):
    __tablename__ = "room"
    id: int | None = Field(default=None, primary_key=True)


class Room(RoomBase):
    id: int


class AttendeeBase(SQLModel):
    name: str = Field(index=True)
    identity_id: str


class AttendeeTable(AttendeeBase, table=True):
    __tablename__ = "attendee"
    id: int | None = Field(default=None, primary_key=True)


class Attendee(AttendeeBase):
    id: int


class PresenterBase(AttendeeBase):
    name: str = Field(index=True)
    website: str


class PresenterTable(PresenterBase, table=True):
    __tablename__ = "presenter"
    id: int | None = Field(default=None, primary_key=True)


class Presenter(PresenterBase):
    id: int


class PanelBase(SQLModel):
    room: str
    start_time: datetime
    end_time: datetime


class PanelTable(PanelBase, table=True):
    __tablename__ = "panel"
    id: int | None = Field(default=None, primary_key=True)


class Panel(PanelBase):
    id: int


class PanelPresenter(SQLModel, table=True):
    panel_id: int = Field(foreign_key="panel.id", primary_key=True)
    presenter_id: int = Field(foreign_key="presenter.id", primary_key=True)


class PanelAttendee(SQLModel, table=True):
    panel_id: int = Field(foreign_key="panel.id", primary_key=True)
    attendee_id: int = Field(foreign_key="attendee.id", primary_key=True)


class ConferenceAttendee(SQLModel, table=True):
    conference_id: int = Field(foreign_key="conference.id", primary_key=True)
    attendee_id: int = Field(foreign_key="attendee.id", primary_key=True)
