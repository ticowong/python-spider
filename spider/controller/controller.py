# _*_ coding:utf-8 _*_

import asyncio
import json
import logging
import random
import time

import CommonPart.commonvar.commonvar

from spider.lib.redis import Redis
from spider.lib.tools import Tools
from spider.model.model import Model
from spider.lib.cookie import Cookie
# from model.user import UserModel
from spider.model.queue_list import QueueList


# from service.api_token import ApiTokenService


class Controller(object):
    """
    控制器类的数据获取函数
    """

    def __init__(self, queue, **kwargs):
        """
        只需要传入队列名即可开启一个爬取任务
        :param queue:
        :param kwargs:
        """
        self.queue = queue
        self.kwargs = kwargs

    async def init(self):
        """
        队列执行入口
        :return:
        """
        try:
            queue = self.queue
            kwargs = self.kwargs
            if not queue:
                queue = 'queue1'
            # 取队列的配置
            queue_list = QueueList(queue)
            if not queue_list:
                logging.error(f"找不到队列{queue}的配置。无法执行队列的数据。")
                return
            self.queue_config = queue_list.get_config()
            queue_key = Tools.dict_get(self.queue_config, 'queue_key')
            if queue_key and Tools.dict_get(kwargs, queue_key):
                self.queue_key = Tools.dict_get(kwargs, queue_key)
            else:
                redis = await Redis().pool()
                if redis:
                    while True:
                        self.queue_key = await queue_list.get_data()
                        if not self.queue_key:
                            logging.info("队列{}为空了。。。".format(queue))
                            await asyncio.sleep(random.randint(1, 3))
                            break
                        # 构造处理中数据的redis缓存键值
                        cache_pre_handing = '{}:handing:{}'.format(
                            Tools.dict_get(self.queue_config, 'cache_pre'), self.queue_key)
                        time_span_out = Tools.dict_get(self.queue_config, 'time_span_out')
                        tmp_uid = await redis.execute("get", cache_pre_handing)
                        if not tmp_uid:
                            logging.info(f"成功从队列{queue}取得{queue_key}：{self.queue_key}")
                            # 如果取到的uid不在处理中，标记
                            await redis.execute("set", cache_pre_handing, '1')
                            await redis.execute("expire", cache_pre_handing, int(time_span_out))
                            break
                        else:
                            ttl = await redis.execute("ttl", cache_pre_handing)
                            if ttl == -1:
                                await redis.execute("expire", cache_pre_handing, int(time_span_out))
                            logging.info(f"成功从队列{queue}取得{queue_key}：{self.queue_key}，但跳过执行。。。")
                            await asyncio.sleep(1)
                            continue
            if self.queue_key:
                tmp = kwargs
                tmp[queue_key] = self.queue_key
                tmp['queue_config'] = self.queue_config
                """启动任务，到execute,然后handleData进行处理"""
                try:
                    logging.info(f"使用参数启动队列任务： {tmp}")
                    await self.run(**tmp)
                except Exception as ex:
                    logging.info(f"启动任务报错： {ex}")
            else:
                logging.info(f"未取得{self.queue}队列里的数据，跳过执行，{__file__}")
        except Exception as ex:
            logging.info({ex})
        finally:
            self.finished()

    async def run(self, **kwargs):
        """
        队列的执行方法
        **kwargs: uid指定执行哪个uid的数据，不传将遍历全部账号
        **kwargs: current，获取第几页的数据，不传则默认第一页
        **kwargs: retry_times,重试次数
        **kwargs: min_page,最少获取几页的数据
        **kwargs: max_page,最多获取几页的数据
        **kwargs: queue_config
        """
        queue_config = Tools.dict_get(kwargs, 'queue_config')
        max_page = Tools.dict_get(queue_config, 'max_page', 10)
        current_page = Tools.dict_get(kwargs, 'current', 1)
        while current_page <= max_page:
            logging.info(f"尝试获取第{current_page}页的数据，{__class__}.execute")
            kwargs['current'] = current_page
            res = await self.execute(**kwargs)
            current_page += 1
            if res:
                break
            await asyncio.sleep(random.randint(1, 3))

    async def getData(self, **kwargs):
        """
        需要重写本函数以获取指定的数据，
        :param kwargs: [current:分页数]
        :return:
        """
        logging.info('需要重写getData函数以获取指定的数据')
        logging.info(f'不能单独执行controller这个父类{kwargs}')
        await asyncio.sleep(0.1)
        return None

    async def handleData(self, response: dict):
        """
        数据处理函数，返回false则跳出循环
        :param response
        :return:
        """
        logging.info(f'{response}')
        logging.info('需要重写handleData函数以处理指定的数据')
        logging.info(f'不能单独执行controller这个父类')
        await asyncio.sleep(0.1)
        return None

    def response_assert(self, resp):
        """
        判断请求是否成功
        :param resp:
        :return:
        """
        if Tools.dict_get(resp, 'status', 0) == 200:
            return True
        logging.info("判断请求为失败，如果成功，请重写response_assert函数")
        return False

    def cookie_assert(self, response):
        """
        判断是否需要调起selenium刷新cookie
        :param response:
        :return:
        """
        if Tools.dict_get(response, 'code') == 403:
            return False
        logging.info("判断请求为需要刷新授权信息，如果不需要取授权信息，请重写cookie_assert函数并返回True")
        return True

    async def execute(self, **kwargs):
        """
        实际执行数据爬取
        :param kwargs:
        :return:
        """
        refresh_cookie = False
        current = Tools.dict_get(kwargs, "current", 1)
        logging.info(f'正在处理第{current}页数据')
        tmp_kwargs = kwargs.copy()
        if 'current' in tmp_kwargs:
            tmp_kwargs.pop("current")
        tmp_kwargs["current"] = current
        # 爬取数据
        queue_config = Tools.dict_get(kwargs, 'queue_config')
        retry_times = Tools.dict_get(queue_config, 'retry_times', 3)
        request_span = Tools.dict_get(queue_config, 'request_span', 1 / 10)
        retry = 1
        while retry <= retry_times:
            try:
                await asyncio.sleep(request_span)
                resp = await self.getData(**tmp_kwargs)
                if queue_config:
                    # 达到配置的最大翻页数，结束遍历
                    max_page = Tools.dict_get(queue_config, 'max_page', 10)
                    if tmp_kwargs["current"] > max_page:
                        return True

                if resp is False:
                    return True
                if resp:
                    logging.info(str(resp)[0:200])
                    if self.response_assert(resp):
                        retry = 1
                        logging.info(f"成功取得{__class__}函数的第{tmp_kwargs['current']}页的数据")
                        logging.info(str(resp)[0:200])
                        # 成功取得数据
                        tmp_res = await self.handleData(resp)
                        if not tmp_res:
                            logging.info(f"跳出翻页循环retry:{retry}...retry_times:{retry_times}")
                            break
                        tmp_kwargs['current'] += 1
                    if not self.cookie_assert(resp):
                        refresh_cookie = True
                elif Tools.dict_get(resp, 'status', 0) == 401:
                    # 取数据失败
                    refresh_cookie = True
                elif Tools.dict_get(resp, 'status', 0) == 402:
                    # 取数据失败
                    refresh_cookie = True
                elif Tools.dict_get(resp, 'status', 0) == 404:
                    # 取数据失败
                    refresh_cookie = True
                else:
                    logging.info(f'error...retry:{retry}...retry_times:{retry_times}')
                    retry += 1
                    continue
            except Exception as ex:
                retry += 1
                logging.info(f"{ex}")
            # 如果cookie过期，重新获取cookie
            if refresh_cookie:
                logging.info("{}的cookie 过期，第{}次自动获取并更新cookie".format("empty users", retry))
                cookie = ""  # await SeleniumLogin().get_weibo_cookie()
                if not cookie:
                    logging.info("获取cookie失败")
                else:
                    # 保存cookie到数据库
                    await Cookie().set(f'uid_{CommonPart.commonvar.commonvar.CommonVar.model_name}', cookie)
                if retry >= retry_times:
                    logging.info(f"尝试{retry}次获取cookie仍失败，需要留意")
                return False
        return True

    def finished(self):
        """
        完成队列的一个协程
        :return:
        """
        parent = Tools.dict_get(self.kwargs, 'parent')
        if parent and hasattr(parent, 'CURRENT_THREADS'):
            if parent.CURRENT_THREADS:
                parent.CURRENT_THREADS[self.queue] -= 1
                left = parent.CURRENT_THREADS[self.queue]
                logging.info(f"完成队列{self.queue}的一个协程,剩下{left}个协程")
        pass

    async def init_queue(self):
        """
        数据入队的操作，指定database,select,table
        :return:
        """
        while True:
            queue = self.queue
            if not queue:
                queue = 'uids'

            # 取队列的配置
            queue_list = QueueList(queue)
            self.queue_config = queue_list.get_config()
            redis = await Redis().pool()
            if redis:
                cache_pre = Tools.dict_get(self.queue_config, 'cache_pre')
                handing_key = "{}:init_queue".format(cache_pre)
                max_length = Tools.dict_get(self.queue_config, 'max_length')
                monitor_filter = Tools.dict_get(self.queue_config, 'monitor_filter', '')
                sql_from_config = Tools.dict_get(self.queue_config, 'sql', '')
                func_queue_source = Tools.dict_get(self.queue_config, 'func_queue_source', False)

                str_database = Tools.dict_get(self.queue_config, 'database', '')
                if not str_database:
                    logging.error("数据入队需要队列的database配置,数据入队操作失败。")
                    break
                str_select = Tools.dict_get(self.queue_config, 'select', '*')
                str_table = Tools.dict_get(self.queue_config, 'table', '')
                if not str_table:
                    logging.error("数据入队需要队列的table配置,数据入队操作失败。")
                    break

                # 队列数据的入队处理间隔
                time_span_in = Tools.dict_get(self.queue_config, 'time_span_in', 1)
                time_span_out = Tools.dict_get(self.queue_config, 'time_span_out', 1)
                time_span_max = time_span_in
                if int(time_span_out) > int(time_span_in):
                    time_span_max = time_span_out

                span_key = f"{cache_pre}:span"
                span = await redis.execute("get", span_key)
                if not span:
                    await redis.execute("set", span_key, '1')
                    await redis.execute("expire", span_key, int(time_span_in))
                else:
                    ttl = await redis.execute("ttl", span_key)
                    if ttl == -1:
                        await redis.execute("expire", span_key, int(time_span_in))
                    await asyncio.sleep(2)
                    continue

                # 队列长度的判断
                length = await redis.execute("llen", cache_pre)
                if length >= 1:
                    logging.info(f'队列有数据，等待下次队列的添加{cache_pre}')
                    await asyncio.sleep(2)
                    continue

                while await redis.execute("llen", cache_pre) >= max_length:
                    logging.info('达到队列极限，等待队列的添加...')
                    await asyncio.sleep(2)

                # 标记和检测当前pod已经在进行入队操作，避免其他队列再操作
                handing = await redis.execute("get", handing_key)
                if handing:
                    logging.info(f'已有其他pod进行队列数据的添加: {cache_pre}')
                    ttl = await redis.execute("ttl", handing_key)
                    if ttl == -1:
                        await redis.execute("expire", handing_key, int(time_span_max))
                    await asyncio.sleep(2)
                    continue

                if func_queue_source:
                    if asyncio.iscoroutinefunction(self.queue_source):
                        list = await self.queue_source()
                    else:
                        list = self.queue_source()
                else:
                    if sql_from_config:
                        sql = sql_from_config
                    else:
                        sql = 'select {str_select} ' \
                              'from {str_table} ' \
                              'where 1 = 1  {monitor_filter}' \
                            .format(str_select=str_select, str_table=str_table, monitor_filter=monitor_filter)
                    list = await Model().list(str_database, sql)

                if list:
                    # 从数据库取到数据后，写入前再次判断，如果已有数据也不再继续，防止多pod因为从数据库读取数据的间歇导致多pod同时写入队列
                    length = await redis.execute("llen", cache_pre)
                    if length >= 1:
                        logging.info(f'队列有数据，等待下次队列的添加: {cache_pre}')
                        await asyncio.sleep(2)
                        continue

                    # 标记和检测当前pod已经在进行入队操作，避免其他队列再操作
                    handing = await redis.execute("get", handing_key)
                    if not handing:
                        await redis.execute("set", handing_key, "1")
                        await redis.execute("expire", handing_key, int(time_span_max))
                    else:
                        ttl = await redis.execute("ttl", handing_key)
                        if ttl == -1:
                            await redis.execute("expire", handing_key, int(time_span_max))
                        logging.info(f'已有其他pod进行队列数据的添加: {cache_pre}')
                        await asyncio.sleep(2)
                        continue

                    for item in list:
                        while await redis.execute("llen", cache_pre) >= max_length:
                            logging.info(f'{queue}达到队列极限，等待队列的添加......')
                            await asyncio.sleep(2)
                        redis.execute("rpush", cache_pre, item[0])

                    # 添加队列完成后删除队列正在添加的标识
                    await redis.execute("del", handing_key)

    async def queue_source(self):
        """
        定义写入队列的数据来源函数，如果队列配置了func_queue_source为True，则本函数需要被重写
        :return:
        """
        logging.error("定义了func_queue_source,控制器的queue_source函数需要重写。")
        await asyncio.sleep(1 / 1000)
        list = {
            ("1"),
            ("2")
        }
        await asyncio.sleep(10)
        return list
