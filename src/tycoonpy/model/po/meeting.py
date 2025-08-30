from datetime import datetime, time

from sqlalchemy import Text
from sqlmodel import Field, Relationship, SQLModel


class Meeting(SQLModel, table=True):
    __tablename__ = "t_linkedin_meeting"

    id: int | None = Field(default=None, primary_key=True)
    subject: str = Field(max_length=255, default="")
    meeting_time: datetime
    meeting_duration: str = Field(max_length=255, default="")
    status: int = 0
    notes: str = Field(sa_type=Text, default="")
    summary_en: str = Field(sa_type=Text, default="")
    summary_cn: str = Field(sa_type=Text, default="")
    user: str = Field(max_length=255, default="")
    source: str = Field(max_length=255, default="")
    country: str = Field(max_length=255, default="")
    contact_tage: str = Field(max_length=255, default="")
    industry: str = Field(max_length=255, default="")
    company: str = Field(max_length=255, default="")
    user_info: str = Field(max_length=255, default="")
    link_address: str = Field(sa_type=Text, default="")
    password: str = Field(max_length=255, default="")
    score: str = Field(max_length=255, default="")

    records: list["MeetingRecord"] = Relationship(back_populates="meeting", cascade_delete=True)


class MeetingRecord(SQLModel, table=True):
    __tablename__ = "t_linkedin_meeting_record"

    id: int | None = Field(default=None, primary_key=True)
    user: str = Field(max_length=255, default="")
    content: str = Field(sa_type=Text, default="")
    content_cn: str = Field(sa_type=Text, default="")
    start_time: time
    end_time: time | None = None

    meeting_id: int | None = Field(default=None, foreign_key="t_linkedin_meeting.id", ondelete="CASCADE")
    meeting: Meeting | None = Relationship(back_populates="records")
