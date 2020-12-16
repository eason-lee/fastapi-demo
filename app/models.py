from typing import List

import arrow
from tortoise import fields, models, Tortoise
from tortoise.contrib.pydantic import PydanticModel
from tortoise.functions import Sum


class StatisticsMeta(models.Model):
    """ meta """

    id = fields.IntField(pk=True)
    project = fields.IntField()
    title = fields.CharField(64)
    belong = fields.CharField(64)
    intro = fields.CharField(128)

    class Meta:
        table = 'statistics_meta'

    @classmethod
    async def add_metas(cls, metas: List[PydanticModel]) -> List[models.Model]:
        """创建 metas"""

        return [
            await StatisticsMeta.create(**d.dict(exclude_unset=True))
            for d in metas
        ]


class StatisticsData(models.Model):
    """ 统计数据 """
    id = fields.IntField(pk=True)
    meta_id = fields.IntField()
    d_t = fields.DatetimeField()
    val = fields.IntField()

    class Meta:
        table = 'statistics_data_v2'
        unique_together = (('meta_id', 'd_t'),)

    @classmethod
    async def get_interval_data(cls,
                                meta_ids: list,
                                start: arrow.Arrow,
                                end: arrow.Arrow) -> list:
        """
        获取时间区内统计数据和
        :param meta_ids:
        :param start:
        :param end:
        :param db:
        :return:
        """
        res = await StatisticsData.filter(
            d_t__gte=start.datetime,
            d_t__lte=end.datetime,
            meta_id__in=meta_ids,
        ).group_by('meta_id').annotate(
            s=Sum('val')
        ).values('meta_id', val='s')

        return res

    @classmethod
    async def get_interval_unit_data(cls,
                                     meta_ids: list,
                                     start: arrow.Arrow,
                                     end: arrow.Arrow,
                                     unit: str) -> list:
        """
        获取
        :param meta_ids:
        :param start:
        :param end:
        :param unit:
        :param db:
        :return:
        """

        """
        由于 tortoise-orm 的问题以下的语句不能使用，所以使用原生 sql 语句

        from pypika import CustomFunction
        from tortoise.expressions import F
        from tortoise.functions import Function

        class TruncTime(Function):
            database_func = CustomFunction(
            "DATE_FORMAT", ["name", "dt_format"])

        unit_fns = {
            'day': TruncTime('d_t', '%Y-%m-%d'),
            'week': TruncTime('d_t', '%x-%v'),
            'month': TruncTime('d_t', '%Y-%m'),
            'year': TruncTime('d_t', '%Y'),
        }

        res = await StatisticsData.filter(
            d_t__gte=start,
            d_t__lte=end,
            meta_id__in=meta_ids,
        ).annotate(
            time=unit_fns.get(unit),
            vals=Sum('val'),
        ).group_by('meta_id', 'time').values(
        'meta_id',time='time', val='vals')

        """
        units = {
            'day': '%Y-%m-%d',
            'week': '%x-%v',
            'month': '%Y-%m',
            'year': '%Y',
        }

        formatter = units.get(unit)
        meta_ids = tuple(set(meta_ids))
        start = start.format()
        end = end.format()
        conn = Tortoise.get_connection("default")
        date_func = f"DATE_FORMAT( `d_t`, '{formatter}' ) `time`"

        from app import debug

        if debug:
            date_func = f"strftime('{formatter}', `d_t` ) `time`"

        sql = f"""
        SELECT
            `meta_id` `meta_id`,
            {date_func},
            SUM( `val` ) `val`
        FROM
            `statistics_data_v2`
        WHERE
            `d_t` >= '{start}'
            AND `d_t` <= '{end}'
            AND `meta_id` IN {meta_ids}
        GROUP BY
            `meta_id`,
            `time`
        """

        res = await conn.execute_query_dict(sql)

        return res
