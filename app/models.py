from peewee import Model, DateTimeField, IntegerField, CompositeKey, fn, Database

from app import get_db, get_db_manager


class StatisticsData(Model):
    """ 统计数据 """

    id = IntegerField()
    d_t = DateTimeField()
    val = IntegerField()

    class Meta:
        database = get_db()
        db_table = 'statistics_data'
        primary_key = CompositeKey('id', 'd_t')

    @classmethod
    async def get_interval_data(cls,
                                meta_ids: list,
                                start: str,
                                end: str,
                                db: Database = None) -> list:
        """
        获取时间区内统计数据和
        :param meta_ids:
        :param start:
        :param end:
        :param db:
        :return:
        """
        # 异步事务的使用
        if not db:
            db = get_db_manager()

        meta_id_q = StatisticsData.id.alias('meta_id')
        query = StatisticsData.select(
            meta_id_q,
            fn.Sum(StatisticsData.val).alias('val')
        ).where(
            StatisticsData.d_t >= start,
            StatisticsData.d_t <= end,
            StatisticsData.id.in_(meta_ids),
        ).group_by(meta_id_q)

        res = await db.execute(
            query.dicts()
        )

        return list(res)

    @classmethod
    async def get_interval_unit_data(cls,
                                     meta_ids: list,
                                     start: str,
                                     end: str,
                                     unit: str,
                                     db: Database = None) -> list:
        """
        获取
        :param meta_ids:
        :param start:
        :param end:
        :param unit:
        :param db:
        :return:
        """
        if not db:
            db = get_db_manager()

        unit_fns = {
            'day': fn.DATE_FORMAT(StatisticsData.d_t, '%Y-%m-%d'),
            'week': fn.YearWeek(StatisticsData.d_t),
            'month': fn.DATE_FORMAT(StatisticsData.d_t, '%Y-%m'),
            'year': fn.Year(StatisticsData.d_t),
        }

        unit_time = unit_fns.get(unit).alias('time')
        query = StatisticsData.select(
            StatisticsData.id.alias('meta_id'),
            unit_time,
            fn.Sum(StatisticsData.val).alias('val')
        ).where(
            StatisticsData.d_t >= start,
            StatisticsData.d_t <= end,
            StatisticsData.id.in_(meta_ids),
        ).group_by(StatisticsData.id, unit_time)

        res = await db.execute(
            query.dicts()
        )
        res = list(res)

        # FIXME peewee_async 会把 date_format 的值变成 datetime
        if unit == 'day':
            for r in res:
                r['time'] = r['time'].strftime('%Y-%m-%d')

        return res
