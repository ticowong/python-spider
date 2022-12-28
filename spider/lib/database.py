# coding = utf-8
import asyncio

import setting
import logging
from CommonPart.kernel.dbnode import AsyncMysqlUtils

DATABASEPOOL = {}

"""
使用本类，需要配置根目录下的setting.py的databases节点下的mysql配置
"""


async def _init():
    global DATABASEPOOL
    while True:
        try:
            for dbs in setting.databases.get('mysql'):
                if not DATABASEPOOL.get(dbs, ''):
                    setting_db = setting.databases.get('mysql').get(dbs)
                    tmp_db = AsyncMysqlUtils()
                    await tmp_db.init_pool(**setting_db)
                    DATABASEPOOL[dbs] = tmp_db
            break
        except Exception as e:
            logging.info(f"连接数据库出错{e}，{__file__}")
            await asyncio.sleep(10)


class DataBase:
    """
    数据库工具类
    """

    def __init__(self):
        pass

    @staticmethod
    async def pool(name=None):
        if not name:
            name = 'mljit'
        await _init()
        tmp = DATABASEPOOL[name]
        return tmp

    async def one(self, db, sql, **kwargs):
        """
        取一条数据
        :param db: 使用数据库
        :param sql: sql语句
        :param kwargs: sql的参数
        :return:
        """

        try:
            cursor = await DataBase.pool(db)
            sql_str = sql.format(**kwargs)
            r = await cursor.select(sql_str)
            if r:
                return r[0]
            return r
        except Exception as e:
            logging.info(f"{__file__},获取数据失败:{e}")
            return None

    async def list(self, db, sql, **kwargs):
        """
        取数据列表
        :param db: 数据库名
        :param sql: sql语句
        :param kwargs: 传入的参数
        :return:
        """
        try:
            cursor = await DataBase.pool(db)
            sql_str = sql.format(**kwargs)
            r = await cursor.select(sql_str)
            return r
        except Exception as e:
            logging.info(f"{__file__},获取数据失败:{e}")
            return None

    async def save(self, db, sql, **kwargs):
        """
        :param db: 数据库名
        :param sql: sql语句
        :param kwargs: 传入sql语句的参数
        :return:
        """
        try:
            cursor = await DataBase.pool(db)
            if not kwargs and len(kwargs):
                sql_str = sql.format(**kwargs)
            else:
                sql_str = sql
            r = await cursor.execute(sql_str)
            return r
        except Exception as e:
            logging.info(f"{__file__},保存数据失败:{e}")
            return None


if __name__ == "__main__":
    tmp = DataBase().one("sample", "select * from ms_cookie limit 1")
    logging.info(tmp)
