# coding = utf-8

import json

from aioredis.pool import ConnectionsPool

import setting
import logging
from spider.lib.json_format import JsonFormat
from CommonPart.kernel.dbnode import AsyncRedisUtils

REDISPOOL = {}

"""
使用本类，需要配置根目录下的setting.py的databases节点下的redis配置
"""


async def init():
    """
        获取任务池连接
        :return: con
        """
    if not REDISPOOL:
        for item in setting.databases.get('redis'):
            redis_tmp = setting.databases.get('redis').get(item)
            account_redis_url = 'redis://:{}@{}:{}/{}'.format(redis_tmp['password'], redis_tmp['host'],
                                                              redis_tmp['port'], redis_tmp['db'])
            redis_obj = AsyncRedisUtils()
            await redis_obj.create_pool(address=account_redis_url)
            try:
                async with redis_obj.redis_pool.get() as tmp_redis:
                    REDISPOOL[item] = tmp_redis
            except Exception as e:
                logging.info("redis连接获取异常...{}".format(e))


class Redis:
    """
    redis 数据库工具类
    """

    async def pool(self, name=None) -> ConnectionsPool:
        if not name:
            name = 'redis_main'
        await init()
        return REDISPOOL[name]

    async def rc_get(self, cache_key, call_back=None, ex=60, *args):
        """
        从缓存取数据，如果没有，使用call_back函数获取并设置到缓存并返回
        :param cache_key: 缓存的键值
        :param call_back: 回调函数或需要缓存并获取的数据
        :param ex: 缓存过期的时间
        :return: 获取的数据
        """
        try:
            redis_pool = await Redis().pool()
            if redis_pool:
                tmp = await redis_pool.execute("get", cache_key)
                if tmp:
                    return json.loads(tmp)
                else:
                    if call_back and callable(call_back):
                        tmp = await call_back(*args)
                        if tmp:
                            await redis_pool.execute("set", cache_key,
                                                     json.dumps(tmp, default=JsonFormat.convert_to_builtin_type,
                                                                check_circular=True)
                                                     )
                            await redis_pool.execute("expire", cache_key, ex)
                            return tmp
                    else:
                        if call_back:
                            json_str = json.dumps(call_back)
                            await redis_pool.execute("set", cache_key, json_str)
                            await redis_pool.execute("expire", cache_key, ex)
                        return call_back
        except Exception as ex:
            logging.log(f"{ex}")
