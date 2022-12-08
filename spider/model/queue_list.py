# _*_ coding:utf-8 _*_

import setting
import logging

from spider.lib.tools import Tools
from spider.lib.redis import Redis


class QueueList(object):
    def __init__(self, queue_name=None):
        if not queue_name:
            queue_name = 'account'
        self.queue_config = Tools.dict_get(setting.queue_list, queue_name)

    def get_config(self):
        return self.queue_config

    async def get_data(self):
        redis = await Redis().pool()
        key = Tools.dict_get(self.queue_config, 'cache_pre')
        tmp = await redis.execute("lpop", key)
        if tmp:
            res = tmp.decode()
            return res


if __name__ == "__main__":
    tmp = QueueList('q1').get_config()
    logging.info(tmp)
    tmp = QueueList().get_data()
    logging.info(tmp)
