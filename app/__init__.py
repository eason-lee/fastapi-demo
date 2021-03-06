import os

from configfile import ConfigFile
from fastapi import FastAPI
from registry import Registry
from tortoise.contrib.fastapi import register_tortoise

"""全局变量"""
service_root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

"""初始化配置"""
GlobalConfigFile = ConfigFile(os.path.join(service_root_path, 'configs'))

server_options = Registry(GlobalConfigFile.load_app('server'))
app_options = Registry(GlobalConfigFile.load_app('app'))

debug = app_options.get('debug').get('active')
mysql_options = server_options.get('mysql_server')


def get_mysql_url(mysql_options, database=None):
    """获取 MySQL DB_URL"""
    if not database:
        database = mysql_options.get('database') or ''

    db_url = 'mysql://{user}:{password}@{host}' \
             ':{port}/{database}?charset={charset}'.format(
                user=mysql_options['user'],
                host=mysql_options['host'],
                port=mysql_options['port'],
                database=database,
                password=mysql_options['password'],
                charset=mysql_options['charset'],
                )
    return db_url


TORTOISE_ORM = {
    "connections": {"default": get_mysql_url(mysql_options),
                    "sqlite": "sqlite://:memory:"},
    "apps": {
        "models": {
            "models": ["app.models", "aerich.models"],
            "default_connection": "default",
        },
    },
}


def create_app(db_conn='default', generate_schemas=False):
    app = FastAPI()
    from . import routers

    # 注册路由
    app.include_router(routers.router)

    # 注册 orm
    register_tortoise(
        app,
        db_url=TORTOISE_ORM['connections'][db_conn],
        modules={"models": TORTOISE_ORM['apps']['models']['models']},
        generate_schemas=generate_schemas,
        add_exception_handlers=True,
    )

    return app


app = create_app()
