from enum import Enum

from pydantic import BaseModel
from tortoise.contrib.pydantic import pydantic_model_creator

from app.models import StatisticsMeta


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


StatisticsMeta_Pydantic = pydantic_model_creator(
    StatisticsMeta,
    name="StatisticsMeta",
)

StatisticsMetaIn_Pydantic = pydantic_model_creator(
    StatisticsMeta,
    name="StatisticsMetaIn",
    exclude_readonly=True,
)
