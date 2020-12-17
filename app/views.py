from typing import List, Optional

import arrow
from fastapi import Query

from app.models import StatisticsData, StatisticsMeta
from app.routers import router
from app.schemas import (IntervalData, TimeUnit, IntervalUnitData,
                         StatisticsMeta_Pydantic,
                         StatisticsMetaIn_Pydantic)


@router.post('/metas',
             status_code=201,
             response_model=List[StatisticsMeta_Pydantic])
async def create_metas(metas: List[StatisticsMetaIn_Pydantic]):
    """

    :param metas:
    :return:
    """
    objs = await StatisticsMeta.add_metas(metas)

    return [await StatisticsMeta_Pydantic.from_tortoise_orm(obj)
            for obj in objs]


@router.get('/metas',
            response_model=List[StatisticsMeta_Pydantic])
async def get_metas(
        ids: Optional[str] = None,
        project_ids: Optional[str] = None,
        title: Optional[str] = Query(None, max_length=64),
        belong: Optional[str] = Query(None, max_length=64),
        intro: Optional[str] = Query(None, max_length=128)
):
    """
    查询 meta
    :param ids: 英文逗号分隔的字符串

    :param project_ids: 英文逗号分隔的字符串

    :param title: 支持模糊查询

    :param belong: 支持模糊查询

    :param intro: 支持模糊查询

    :return:
    """
    lookup = {}

    if ids is not None:
        ids = ids.split(',')
        lookup['id__in'] = ids
    if project_ids is not None:
        project_ids = project_ids.split(',')
        lookup['project__in'] = project_ids
    if title:
        lookup['title__icontains'] = title
    if belong:
        lookup['belong__icontains'] = belong
    if intro:
        lookup['intro__icontains'] = intro

    res = StatisticsMeta.filter(**lookup)

    return await StatisticsMeta_Pydantic.from_queryset(res)


@router.get('/interval', response_model=List[IntervalData])
async def get_interval_data(meta_ids: str,
                            start: str,
                            end: str):
    """
    获取某时间段内的统计数据和

    :param meta_ids: 请求的 meta_ids, 以英文 , 分隔的字符串

    :param day: 开始时间，例如 2020-12-01

    :param end: 结束时间，例如 2020-12-01

    :param db: 数据库连接，不需要传

    :return:
    """
    start = arrow.get(start).floor('day')
    end = arrow.get(end).ceil('day')
    meta_ids = meta_ids.split(',')

    res = await StatisticsData.get_interval_data(meta_ids,
                                                 start,
                                                 end)
    return res


@router.get('/interval/unit', response_model=List[IntervalUnitData])
async def get_interval_of_unit_data(meta_ids: str,
                                    start: str,
                                    end: str,
                                    unit: TimeUnit):
    """
    获取某时间段内根据某时间单位分组的统计数据

    :param meta_ids: 请求的 meta_ids, 以英文 , 分隔的字符串

    :param day: 开始时间，例如 2020-12-01

    :param end: 结束时间，例如 2020-12-01

    :param unit: 时间单位

    :param db: 数据库连接，不需要传

    :return:
    """
    start = arrow.get(start).floor('day')
    end = arrow.get(end).ceil('day')
    meta_ids = meta_ids.split(',')

    res = await StatisticsData.get_interval_unit_data(meta_ids,
                                                      start,
                                                      end,
                                                      unit)

    return res
