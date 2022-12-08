# _*_ coding:utf-8 _*_


import re
import time
import datetime
import asyncio
import logging
import setting
from spider.lib.redis import Redis
from spider.lib.tools import Tools
from CommonPart.commonvar.commonvar import CommonVar
from CommonPart.combuiltin.combuiltin import ComBuiltin
from spider.controller.database import DataBaseController


class Main:
    CURRENT_THREADS = {}

    @staticmethod
    async def run(start_queue=""):
        logging.info(f"Start {start_queue}")

        tasks = list()
        redis = await Redis().pool()
        db_queue_key = f"{CommonVar.model_name}:db:queue"
        db_queue = await redis.execute("get", db_queue_key)
        if not db_queue:
            """一个pod独占异步落库脚本"""
            logging.info("当前pod将被落库任务独占使用，否则请重启")
            await redis.execute("set", db_queue_key, ComBuiltin.get_current_time())
            await redis.execute("expire", db_queue_key, 60 * 5)
            # 数据库异步落库
            for str_db in setting.database_queue_list:
                task_db = asyncio.create_task(DataBaseController(str_db).handle())
                tasks.append(task_db)
        else:
            """其他pod执行爬取任务"""
            # 执行全部队列
            task_configs = Main.task_config()
            for queue_tmp in task_configs:
                if not start_queue or queue_tmp in start_queue:
                    # 按队列，对数据的爬取
                    task_tmp = asyncio.create_task(Main.handle(queue_tmp, task_configs[queue_tmp].__name__))
                    tasks.append(task_tmp)
                    # 添加数据到队列
                    task_tmp = asyncio.create_task(task_configs[queue_tmp](queue_tmp).init_queue())
                    tasks.append(task_tmp)

            """数据库异步落库"""
            for str_db in setting.database_queue_list:
                task_db = asyncio.create_task(DataBaseController(str_db).handle())
                tasks.append(task_db)

        await asyncio.gather(*tasks)

        while True:
            logging.info(f"{CommonVar.model_name} in waiting...")
            await asyncio.sleep(10)

    def task_config(self) -> dict:
        """队列名和对应的控制器名"""
        res = {}
        logging.error("需要重写spider.controller.Main类的task_config")
        return res

    @staticmethod
    async def handle(queue_name, controller_name):
        """
        处理队列数据
        :return:
        """
        queue_config = setting.queue_list.get(queue_name)
        max_thread = Tools.dict_get(queue_config, 'max_thread', 3)

        while True:
            if not Tools.dict_get(Main.CURRENT_THREADS, queue_name):
                Main.CURRENT_THREADS[queue_name] = 0
            now = Main.CURRENT_THREADS[queue_name]
            if now < max_thread:
                # 启动任务
                Main.CURRENT_THREADS[queue_name] += 1
                eval(
                    f"asyncio.create_task(controller.{controller_name}(queue_name, parent={__class__.__name__}).init())")
                now = Main.CURRENT_THREADS[queue_name]
                logging.info(f"启动队列{queue_name}的第{now}个协程,最大{max_thread}个协程。")
            else:
                await asyncio.sleep(1)
