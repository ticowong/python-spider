# _*_ coding:utf-8 _*_

import asyncio
import json
import logging
import random
import time

import setting

from spider.lib.database import DataBase
from spider.lib.tools import Tools
from spider.lib.redis import Redis
from CommonPart.commonvar.commonvar import CommonVar
from CommonPart.combuiltin.combuiltin import ComBuiltin


class DataBaseController(object):
    """
    异步落库控制器
    """

    def __init__(self, queue="database"):
        self.queue_name = queue
        pass

    async def push(self, sql):
        """
        将sql语句入队
        :param sql:
        :return:
        """
        redis = await Redis().pool()
        if redis:
            queue_config = setting.database_queue_list.get(self.queue_name)
            cache_pre = Tools.dict_get(queue_config, 'cache_pre')
            max_length = Tools.dict_get(queue_config, 'max_length', 100000)
            while True:
                try:
                    now_len = await redis.execute("llen", cache_pre)
                    if now_len >= max_length:
                        await asyncio.sleep(1)
                        continue
                    else:
                        break
                except Exception as ex:
                    logging.error(f"{ex}")
                    break
            await redis.execute("rpush", cache_pre, sql)

    async def handle(self):
        """
        将队列数据落库守护启动
        :return:
        """
        while True:
            try:
                await self.run()
            except Exception as ex:
                logging.info(f"异步将队列落库异常{ex}")
            await asyncio.sleep(random.randint(1, 3))

    async def run(self):
        """
        将队列数据落库的实际操作
        :return:
        """
        max_index = 50
        redis = await Redis().pool()
        if redis:
            queue_config = setting.database_queue_list.get(self.queue_name)
            cache_pre = Tools.dict_get(queue_config, 'cache_pre')
            db_name = Tools.dict_get(queue_config, 'db_name', 'weibo')
            while True:
                db_queue_key = f"{CommonVar.model_name}:db:queue"
                try:
                    await redis.execute("set", db_queue_key, ComBuiltin.get_current_time())
                    await redis.execute("expire", db_queue_key, 60 * 5)
                except Exception as ex:
                    logging.info(f"{ex}")
                sql = ''
                index = 0
                while index < max_index:
                    index += 1
                    try:
                        tmp_sql = await redis.execute("lpop", cache_pre)
                        if not tmp_sql:
                            break
                        if sql:
                            sql = f"{bytes.decode(tmp_sql)};{sql}"
                        else:
                            sql = f"{bytes.decode(tmp_sql)}"
                    except Exception as ex:
                        logging.info(f"{ex}")
                if sql:
                    try:
                        res = await DataBase().save(db_name, sql)
                        logging.info(sql)
                        if res:
                            logging.info('数据异步落库成功')
                        else:
                            logging.info('数据异步落库失败')
                    except Exception as ex:
                        logging.info(f"数据异步落库失败:{ex}")
                else:
                    await asyncio.sleep(1)
