import asyncio
from typing import Generator

import pytest
from fastapi.testclient import TestClient

from tortoise.contrib.test import finalizer, initializer

from app import app
from app.models import StatisticsData


@pytest.fixture
def client() -> Generator:
    # 初始化数据库
    initializer(["app.models"])
    with TestClient(app) as c:
        yield c

    # 测试完后清除数据
    finalizer()


async def create_statistics_data():
    await StatisticsData.create(
        meta_id=1,
        d_t='2020-12-08 01:12',
        val=10,
    )
    await StatisticsData.create(
        meta_id=1,
        d_t='2020-12-08 02:23',
        val=10,
    )
    await StatisticsData.create(
        meta_id=2,
        d_t='2020-11-09',
        val=10,
    )
    await StatisticsData.create(
        meta_id=2,
        d_t='2020-12-09',
        val=10,
    )
    await StatisticsData.create(
        meta_id=3,
        d_t='2020-12-10',
        val=10,
    )

    return


def test_get_interval_data(client: TestClient):

    event_loop = asyncio.get_event_loop()
    event_loop.run_until_complete(create_statistics_data())

    start = '2020-11-01'
    end = '2020-12-20'
    response = client.get("/v1/statistics/interval",
                          params={'meta_ids': '1,2,3',
                                  'start': start,
                                  'end': end})

    assert response.status_code == 200, response.text
    data = response.json()

    for d in data:
        if d.get('meta_id') == 1:
            assert d.get('val') == 20
        if d.get('meta_id') == 2:
            assert d.get('val') == 20
        if d.get('meta_id') == 3:
            assert d.get('val') == 10


def test_get_interval_unit_data(client: TestClient):
    event_loop = asyncio.get_event_loop()
    event_loop.run_until_complete(create_statistics_data())

    start = '2020-11-01'
    end = '2020-12-20'
    # day
    response = client.get("/v1/statistics/interval/unit",
                          params={'meta_ids': '1,2,3',
                                  'start': start,
                                  'end': end,
                                  'unit': 'day'})

    assert response.status_code == 200, response.text
    data = response.json()

    for d in data:
        if d.get('meta_id') == 1:
            assert d.get('val') == 20
        if d.get('meta_id') == 2:
            assert d.get('val') == 10
        if d.get('meta_id') == 3:
            assert d.get('val') == 10

    # month
    response = client.get("/v1/statistics/interval/unit",
                          params={'meta_ids': '1,2,3',
                                  'start': start,
                                  'end': end,
                                  'unit': 'month'})

    assert response.status_code == 200, response.text
    data = response.json()

    for d in data:
        if d.get('meta_id') == 1:
            assert d.get('val') == 20
        if d.get('meta_id') == 2:
            assert d.get('val') == 10
        if d.get('meta_id') == 3:
            assert d.get('val') == 10

    # year
    response = client.get("/v1/statistics/interval/unit",
                          params={'meta_ids': '1,2,3',
                                  'start': start,
                                  'end': end,
                                  'unit': 'year'})

    assert response.status_code == 200, response.text
    data = response.json()

    for d in data:
        if d.get('meta_id') == 1:
            assert d.get('val') == 20
        if d.get('meta_id') == 2:
            assert d.get('val') == 20
        if d.get('meta_id') == 3:
            assert d.get('val') == 10
