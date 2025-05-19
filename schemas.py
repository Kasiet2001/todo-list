from pydantic import BaseModel, field_validator
from datetime import date
from typing import Optional
from enum import Enum


class StatusEnum(str, Enum):
    NEW = "NEW"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"


def validate_status(cls, status):
    status = status.replace(' ', '_').upper()
    return StatusEnum(status)


class TaskBase(BaseModel):
    title: str
    description: Optional[str]
    due_date: date
    status: StatusEnum

    @field_validator('status', mode='before')
    def validate_task_status(cls, value):
        return validate_status(cls, value)

    @field_validator('due_date', mode='before')
    def validate_due_date(cls, value):
        if isinstance(value, str):
            try:
                value = date.fromisoformat(value)
            except ValueError:
                raise ValueError("Date format must be YYYY-MM-DD")
        if value < date.today():
            raise ValueError("Due date must be in the future")
        return value


class TaskUpdate(BaseModel):
    title: str = None
    description: Optional[str] = None
    due_date: date = None
    status: StatusEnum = None

    @field_validator('status', mode='before')
    def validate_task_update_status(cls, value):
        return validate_status(cls, value)

    @field_validator('due_date', mode='before')
    def validate_due_date(cls, value):
        if isinstance(value, str):
            try:
                value = date.fromisoformat(value)
            except ValueError:
                raise ValueError("Date format must be YYYY-MM-DD")
        return value
