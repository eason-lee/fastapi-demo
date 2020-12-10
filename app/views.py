from typing import List

import arrow
from fastapi import Depends
from peewee import Database

from app import get_db_manager
from app.models import StatisticsData
from app.routers import router
from app.schemas import IntervalData, TimeUnit, IntervalUnitData


@router.get('/interval', response_model=List[IntervalData])
async def get_interval_data(meta_ids: str,
                            start: str,
                            end: str,
                            db: Database = Depends(get_db_manager)):
    """
    获取某时间段内的统计数据和

    :param meta_ids: 请求的 meta_ids, 以英文 , 分隔的字符串

    :param day: 开始时间，例如 2020-12-01

    :param end: 结束时间，例如 2020-12-01

    :param db: 数据库连接，不需要传

    :return:
    """
    start = arrow.get(start).floor('day').format()
    end = arrow.get(end).ceil('day').format()
    meta_ids = meta_ids.split(',')

    res = await StatisticsData.get_interval_data(meta_ids,
                                                 start,
                                                 end,
                                                 db=db)

    return res


@router.get('/interval/unit', response_model=List[IntervalUnitData])
async def get_interval_of_unit_data(meta_ids: str,
                                    start: str,
                                    end: str,
                                    unit: TimeUnit,
                                    db: Database = Depends(get_db_manager)):
    """
    获取某时间段内根据某时间单位分组的统计数据

    :param meta_ids: 请求的 meta_ids, 以英文 , 分隔的字符串

    :param day: 开始时间，例如 2020-12-01

    :param end: 结束时间，例如 2020-12-01

    :param unit: 时间单位

    :param db: 数据库连接，不需要传

    :return:
    """
    start = arrow.get(start).floor('day').format()
    end = arrow.get(end).ceil('day').format()
    meta_ids = meta_ids.split(',')

    res = await StatisticsData.get_interval_unit_data(meta_ids,
                                                      start,
                                                      end,
                                                      unit,
                                                      db=db)

    return res
