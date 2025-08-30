import logging
import re
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import webvtt
from hpyhrtbase import hpyhrt_context
from sqlmodel import Session, select

from tycoonpy.app.tycoon_app import tycoon_app_setup
from tycoonpy.model.po import Meeting, MeetingRecord
from tycoonpy.model.po.database import get_engine

mod_logger = logging.getLogger(__name__)

def meeting_record_import() -> None:
    mod_logger.info("Enter")

    config_inst = hpyhrt_context.get_config_inst()

    webvtt_files_dir = Path(config_inst.webvtt_files_dir)

    if not webvtt_files_dir.exists() or not webvtt_files_dir.is_dir():
        mod_logger.error(f"invalid dir path {webvtt_files_dir}")
        return

    chat_line_pattern = r"""
        ^(\d{2}:\d{2}:\d{2})  # 时间部分 (HH:MM:SS)
        \s+                   # 任意数量的空白字符
        ([A-Za-z\s'.-]+)      # 人名部分
        :                     # 冒号
        \s+                   # 冒号后的任意数量空白字符
        .*$                   # 后面可以跟其他内容
    """

    with Session(get_engine()) as session:
        for file_path in webvtt_files_dir.rglob("*.vtt"):
            if not file_path.is_file():
                continue

            mod_logger.info(f"file_name {file_path.name}")

            meeting_time_str = file_path.name.split("_Recording", 1)[0][3:]

            meeting_time = datetime.strptime(meeting_time_str, "%Y%m%d-%H%M%S").replace(tzinfo=ZoneInfo("UTC"))
            mod_logger.info(f"meeting_time {meeting_time.isoformat()}")

            statement = select(Meeting).where(Meeting.meeting_time == meeting_time)
            results  = session.exec(statement)
            meeting = results.first()

            if meeting is None:
                meeting = Meeting(meeting_time=meeting_time)
                session.add(meeting)
                session.commit()
                session.refresh(meeting)

            record_statement = select(MeetingRecord).where(MeetingRecord.meeting_id == meeting.id)
            records = session.exec(record_statement).all()
            read_idx = 0
            webrtt_inst = webvtt.read(file_path)
            time_format = "%H:%M:%S.%f"
            user_list: list[str] = []

            if len(records) < len(webrtt_inst):
                for caption in webrtt_inst:
                    start_time = datetime.strptime(caption.start, time_format).time()
                    end_time = datetime.strptime(caption.end, time_format).time()
                    user, content = caption.text.split(": ", 1)
                    if user not in user_list:
                        user_list.append(user)
                    while read_idx < len(records) and records[read_idx].start_time < start_time:
                        read_idx += 1
                    if read_idx < len(records) and records[read_idx].start_time == start_time:
                        continue
                    meeting_record = MeetingRecord(start_time=start_time, end_time=end_time, user=user, content=content, meeting=meeting)
                    session.add(meeting_record)

            if not meeting.subject:
                meeting.subject = " and ".join(user_list)
                session.add(meeting)
                session.commit()
                session.refresh(meeting)

            chat_path = webvtt_files_dir / f"GMT{meeting_time_str}_RecordingnewChat.txt"

            if chat_path.exists():
                read_idx = 0
                last_record: MeetingRecord | None = None
                with open(chat_path, encoding="utf-8") as fh:
                    lines = fh.readlines()
                for line in lines:
                    match = re.match(chat_line_pattern, line, re.VERBOSE)
                    if not match:
                        if last_record:
                            last_record.content += line
                        continue
                    if last_record:
                        last_record.content = last_record.content.strip()
                        session.add(last_record)
                        last_record = None
                    start_time_str, other = line.split(maxsplit=1)
                    start_time = datetime.strptime(start_time_str, "%H:%M:%S").time()
                    user, content = re.split(r":\s+", other, maxsplit=1)
                    while read_idx < len(records) and records[read_idx].start_time < start_time:
                        read_idx += 1
                    if read_idx < len(records) and records[read_idx].start_time == start_time:
                        continue
                    meeting_record = MeetingRecord(start_time=start_time, user=user, content=content, meeting=meeting)
                    last_record = meeting_record

                if last_record:
                    last_record.content = last_record.content.strip()
                    session.add(last_record)

            session.commit()

    mod_logger.info("Leave")

if __name__ == "__main__":
    tycoon_app_setup()

    meeting_record_import()
