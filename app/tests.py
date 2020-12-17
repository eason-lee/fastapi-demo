import asyncio
from typing import Generator

import pytest
from faker import Faker
from fastapi.testclient import TestClient
from tortoise.contrib.test import finalizer, initializer

from app import create_app
from app.models import StatisticsData

fake = Faker()


@pytest.fixture
def client() -> Generator:
    app = create_app(db_conn='sqlite',
                     generate_schemas=True)
    # 初始化数据库
    initializer(['app.models'])

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


def test_get_interval_data(client: TestClient):
    event_loop = asyncio.get_event_loop()
    event_loop.run_until_complete(create_statistics_data())

    start = '2020-11-01'
    end = '2020-12-20'
    response = client.get('/v1/statistics/interval',
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
    response = client.get('/v1/statistics/interval/unit',
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
    response = client.get('/v1/statistics/interval/unit',
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
    response = client.get('/v1/statistics/interval/unit',
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


def test_create_metas(client: TestClient):
    data = [{
        'project': 1,
        'title': '测试1',
        'belong': 'test--1',
        'intro': 'test1',
    }]

    response = client.post('/v1/statistics/metas',
                           json=data)

    assert response.status_code == 201
    result = response.json()[0]
    assert result['project'] == data[0]['project']
    assert result['title'] == data[0]['title']
    assert result['belong'] == data[0]['belong']
    assert result['intro'] == data[0]['intro']


def test_get_metas(client: TestClient):
    data1 = {
        'project': 1,
        'title': '测试{}'.format(fake.name()),
        'belong': '冒险{}'.format(fake.name()),
        'intro': 'test ',
    }
    data2 = {
        'project': 2,
        'title': '测试{}'.format(fake.name()),
        'belong': '{}军事'.format(fake.name()),
        'intro': '冬休 ',
    }
    data3 = {
        'project': 3,
        'title': '没有{}'.format(fake.name()),
        'belong': '哈哈{}'.format(fake.name()),
        'intro': '词典 {}'.format(fake.name()),
    }

    client.post('/v1/statistics/metas', json=[data1, data2, data3])

    response = client.get('/v1/statistics/metas',
                          params={
                              'project_ids': '1,2,3'
                          })

    assert response.status_code == 200
    result = response.json()
    assert len(result) == 3

    response = client.get('/v1/statistics/metas',
                          params={
                              'title': '测试'
                          })
    result = response.json()
    assert len(result) == 2

    response = client.get('/v1/statistics/metas',
                          params={
                              'title': '没有'
                          })
    result = response.json()
    assert len(result) == 1
    assert result[0]['belong'] == data3['belong']
    assert result[0]['intro'] == data3['intro']
    assert result[0]['project'] == data3['project']

    response = client.get('/v1/statistics/metas',
                          params={
                              'belong': '军事'
                          })
    result = response.json()
    assert len(result) == 1

    response = client.get('/v1/statistics/metas',
                          params={
                              'intro': '词典'
                          })
    result = response.json()
    assert len(result) == 1
