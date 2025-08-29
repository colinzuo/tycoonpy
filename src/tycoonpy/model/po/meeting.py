from datetime import time

from sqlmodel import Field, SQLModel


class Meeting(SQLModel, table=True):
    __tablename__ = "t_linkedin_meeting"

    id: int | None = Field(default=None, primary_key=True)
    subject: str = ""
    meeting_time: str = ""
    status: int = 0
    notes: str = ""
    summary_en: str = ""
    user: str = ""
    source: str = ""
    country: str = ""
    contact_tage: str = ""
    industry: str = ""
    company: str = ""
    user_info: str = ""
    link_address: str = ""
    password: str = ""
    summary_cn: str = ""
    score: str = ""


class MeetingRecord(SQLModel, table=True):
    __tablename__ = "t_linkedin_meeting_record"

    id: int | None = Field(default=None, primary_key=True)
    user: str = ""
    content_en: str = ""
    content_cn: str = ""
    meeting_id: int = 0
    date_time: time | None = None
