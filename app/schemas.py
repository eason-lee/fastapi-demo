from enum import Enum

from pydantic import BaseModel


class TimeUnit(str, Enum):
    day = 'day'
    week = 'week'
    month = 'month'
    year = 'year'


class IntervalData(BaseModel):
    meta_id: int
    val: float


class IntervalUnitData(BaseModel):
    meta_id: int
    time: str
    val: float
