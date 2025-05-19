from sqlalchemy import Column, Integer, String, Date, Enum
from sqlalchemy.orm import declarative_base
import enum

Base = declarative_base()


class TaskStatus(str, enum.Enum):
    NEW = "NEW"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    title = Column(String, index=True)
    description = Column(String)
    due_date = Column(Date)
    status = Column(Enum(TaskStatus))


