import os

import peewee_async
from configfile import ConfigFile
from fastapi import FastAPI
from registry import Registry

"""全局变量"""
service_root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

"""初始化配置"""
GlobalConfigFile = ConfigFile(os.path.join(service_root_path, 'configs'))

server_options = Registry(GlobalConfigFile.load_app('server'))
app_options = Registry(GlobalConfigFile.load_app('app'))

mysql_options = server_options.get('mysql_server')
debug = app_options.get('debug').get('active')


def get_db():
    # peewee_async 暂时不支持 sqlite
    # if debug:
    #     db_url = 'sqlite:///sqlite3.db'
    #     db = peewee_async.SqliteDatabase(db_url)
    # else:

    # peewee_async 会使用 aiomysql 创建连接池
    db = peewee_async.MySQLDatabase(
        user=mysql_options['user'],
        host=mysql_options['host'],
        port=mysql_options['port'],
        database=mysql_options.get('database') or '',
        password=mysql_options['password'],
        charset=mysql_options['charset'],
        pool_recycle=3600,
    )
    db.set_allow_sync(False)

    return db


def get_db_manager(db=None):
    if not db:
        db = get_db()
    # peewee_async.Manager 会自动管理连接池
    return peewee_async.Manager(db)


def create_app():
    app = FastAPI()
    from . import routers
    # 注册路由
    app.include_router(routers.router)

    return app


app = create_app()
