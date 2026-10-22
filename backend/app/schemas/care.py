"""Pydantic v2 request/response models."""
import re
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator

HHMM = re.compile(r"^([01]\d|2[0-3]):[0-5]\d$")


class MedicationIn(BaseModel):
    name: str = Field(min_length=1, max_length=80)
    aliases: list[str] = Field(default_factory=list, max_length=12)
    dose: str | None = Field(default=None, max_length=60)
    times: list[str] = Field(min_length=1, max_length=8)

    @field_validator("times")
    @classmethod
    def _times(cls, v: list[str]) -> list[str]:
        if any(not HHMM.match(t) for t in v):
            raise ValueError("times must look like 08:30")
        return sorted(set(v))

    @field_validator("name")
    @classmethod
    def _strip(cls, v: str) -> str:
        return v.strip()


class MedicationOut(MedicationIn):
    model_config = ConfigDict(from_attributes=True)
    id: int


class AppointmentIn(BaseModel):
    title: str = Field(min_length=1, max_length=120)
    starts_at: datetime


class AppointmentOut(AppointmentIn):
    model_config = ConfigDict(from_attributes=True)
    id: int


class ContactIn(BaseModel):
    name: str = Field(min_length=1, max_length=80)
    telegram_chat_id: str | None = Field(default=None, max_length=40, pattern=r"^-?\d+$")
    role: str | None = Field(default=None, max_length=40)


class ContactOut(ContactIn):
    model_config = ConfigDict(from_attributes=True)
    id: int


class EventOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    type: str
    severity: str
    message: str
    created_at: datetime
    notified: bool
    delivery: str


class ToolCallOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    tool_name: str
    inputs: dict[str, object]
    result: str
    duration_ms: int
    success: bool
    source: str
    created_at: datetime


class ChatIn(BaseModel):
    text: str = Field(min_length=1, max_length=500)


class ToolCallRecordOut(BaseModel):
    name: str
    arguments: dict[str, object]
    result: str
    duration_ms: int
    success: bool


class ChatOut(BaseModel):
    reply: str
    tool_calls: list[ToolCallRecordOut]
    used_llm: bool
