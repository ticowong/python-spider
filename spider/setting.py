# _*_ coding:utf-8 _*_

'''''
信息配置示例文件
文件请放项目跟目录
'''''

databases = {
    'mysql': {
        # adb数据库
        'biadb': {
            'host': '127.0.0.1',
            'port': 3306,
            'db': 'sample',
            'user': 'root',
            'password': 'root',
            'charset': 'utf8mb4',
            'autocommit': True
        },
    },
    'redis': {
        # redis数据库
        'redis_main': {
            'host': '127.0.0.1',
            'port': 6379,
            'db': 0,
            'password': '',
            'decode_responses': True
        }
    }
}


"""
0为所有级别提示都展示，
1为展示notice级提示和waring级和error级和钉钉提示级信息，
2为展示warning级提示和error级钉钉提示级信息,
3为展示error级和钉钉提示级信息，
4为只展示钉钉通知级别信息，
大于4则不展示任何信息
"""
logging_level = 0

"""
队列配置
每个队列配置都作为一个独立数据爬取任务
"""
queue_list = {
    'queue_001': {
        # 队列的key值
        'cache_pre': 'queue:queue_001',
        # 队列最大存储量
        'max_length': 1000,
        # 爬取最少翻页数
        'min_page': 1,
        # 爬取最大翻页数
        'max_page': 1,
        # 每次爬取失败的重试次数
        'retry_times': 3,
        # 每次请求间的间隔(秒)
        'request_span': 1 / 100,
        # 最大线程数
        'max_thread': 2,
        # 监控几天内的数据
        'monitor_days': 30,
        # 写入数据到对列的间隔时间
        'time_span_in': 30,
        # 取队列数据，并处理数据的间隔时间
        'time_span_out': 60 * 1,
        # 队列数据的来源数据库
        'database': 'it_main',
        # 队列数据的来源数据表
        'table': 'ho_account',
        # 队列数据的来源数据列
        'select': 'uid',
        # 队列使用的列名关键字， 必须配置
        'queue_key': 'uid',
        # 队列数据的来源数据表的限制条件
        'monitor_filter': ' ',
        # 取队列数据使用的sql语句，可选配置
        'sql': "",
        # 队列数据是否来自于自定义的queue_source函数，需要返回可遍历数据，可选配置,若设置True则优先级最高，sql次之，最后monitor_filter
        'func_queue_source': True,
    },
}

database_queue_list = {
    # 定义数据库落库队列
    'database': {
        # 使用示例：await spider.controller.DataBaseController("database").push(sql)
        # 异步落库队列
        'cache_pre': 'data:list',
        # 队列最大存储量,到限制就等着，防止redis撑爆
        'max_length': 200000,
        # 队列落库数据库名
        'db_name': 'sample',
    },
}

#  请求头切换列表
ua_list = [
    'Mozilla/5.0 (Linux; U; Android 7.1.2; zh-cn; Redmi 4X Build/N2G47H) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/71.0.3578.141 Mobile Safari/537.36 XiaoMi/MiuiBrowser/11.8.14',
    'Mozilla/5.0 (Linux; Android 7.0; TRT-AL00 Build/HUAWEITRT-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/76.0.3809.89 Mobile Safari/537.36 T7/11.21 SP-engine/2.17.0 baiduboxapp/11.21.0.10 (Baidu; P1 7.0)',
    'Mozilla/5.0 (Linux; Android 7.1.2; Redmi Note 5A Build/N2G47H; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/63.0.3239.83 Mobile Safari/537.36 T7/10.13 baiduboxapp/10.13.0.11 (Baidu; P1 7.1.2)',
    'Mozilla/5.0 (Linux; Android 9; GLK-AL00 Build/HUAWEIGLK-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/76.0.3809.89 Mobile Safari/537.36 T7/11.21 SP-engine/2.17.0 baiduboxapp/11.21.0.10 (Baidu; P1 9) NABar/1.0',
    'Mozilla/5.0 (Linux; U; Android 8.0.0; zh-CN; SM-G9350 Build/R16NW) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/12.5.9.1039 Mobile Safari/537.36',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 13_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/6.7.3(0x16070321) NetType/WIFI Language/zh_CN',
    'Mozilla/5.0 (Linux; Android 8.0.0; KNT-AL20 Build/HUAWEIKNT-AL20; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/76.0.3809.89 Mobile Safari/537.36 T7/11.21 SP-engine/2.17.0 baiduboxapp/11.21.0.10 (Baidu; P1 8.0.0) NABar/1.0',
    'Mozilla/5.0 (Linux; Android 9; Redmi Note 5 Build/PKQ1.180904.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/76.0.3809.89 Mobile Safari/537.36 T7/11.21 SP-engine/2.17.0 baiduboxapp/11.21.0.10 (Baidu; P1 9) NABar/1.0',
    'Mozilla/5.0 (Linux; Android 8.1.0; JKM-AL00a Build/HUAWEIJKM-AL00a; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/76.0.3809.89 Mobile Safari/537.36 T7/11.21 SP-engine/2.17.0 baiduboxapp/11.21.0.10 (Baidu; P1 8.1.0)',
    'Mozilla/5.0 (Linux; U; Android 9; zh-cn; INE-AL00 Build/HUAWEIINE-AL00) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/66.0.3359.126 MQQBrowser/10.2 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; U; Android 9; zh-CN; MI 9 SE Build/PKQ1.181121.001) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/12.8.0.1060 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; U; Android 10; zh-cn; Mi 10 Build/QKQ1.191117.002) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/71.0.3578.141 Mobile Safari/537.36 XiaoMi/MiuiBrowser/11.10.14',
    'Mozilla/5.0 (Linux; Android 9; DUK-AL20 Build/HUAWEIDUK-AL20; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/76.0.3809.89 Mobile Safari/537.36 T7/11.21 SP-engine/2.17.0 baiduboxapp/11.21.0.10 (Baidu; P1 9)',
    'Mozilla/5.0 (Linux; U; Android 10; zh-CN; TAS-AN00 Build/HUAWEITAS-AN00) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/12.0.2.995 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; U; Android 9; zh-CN; ONEPLUS A5000 Build/PKQ1.180716.001) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/12.9.2.1072 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 7.0; STF-AL10 Build/HUAWEISTF-AL10; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/66.0.3359.126 MQQBrowser/6.2 TBS/045132 Mobile Safari/537.36 V1_AND_SQ_8.2.6_1320_YYB_D QQ/8.2.6.4370 NetType/4G WebP/0.3.0 Pixel/1080 StatusBarHeight/72 SimpleUISwitch/0',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 13_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/7.0.12(0x17000c23) NetType/WIFI Language/zh_CN',
    'Mozilla/5.0 (Linux; U; Android 9; zh-cn; MI MAX 3 Build/PKQ1.181007.001) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/61.0.3163.128 Mobile Safari/537.36 XiaoMi/MiuiBrowser/10.4.8',
    'Mozilla/5.0 (Linux; U; Android 9; zh-CN; YAL-AL50 Build/HUAWEIYAL-AL50) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/12.9.2.1072 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 9; VRD-AL09 Build/HUAWEIVRD-AL09; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/76.0.3809.89 Mobile Safari/537.36 T7/11.21 SP-engine/2.17.0 baiduboxapp/11.21.0.10 (Baidu; P1 9) NABar/1.0',
    'Mozilla/5.0 (Linux; Android 8.0.0; WAS-TL10 Build/HUAWEIWAS-TL10; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/76.0.3809.89 Mobile Safari/537.36 T7/11.21 SP-engine/2.17.0 baiduboxapp/11.21.0.10 (Baidu; P1 8.0.0)',
    'Mozilla/5.0 (Linux; Android 10; OXF-AN10 Build/HUAWEIOXF-AN10; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/76.0.3809.89 Mobile Safari/537.36 T7/11.21 SP-engine/2.17.0 baiduboxapp/11.21.0.10 (Baidu; P1 10)',
    'Mozilla/5.0 (Linux; Android 9; COR-AL10 Build/HUAWEICOR-AL10; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/76.0.3809.89 Mobile Safari/537.36 T7/11.21 SP-engine/2.17.0 baiduboxapp/11.21.0.10 (Baidu; P1 9) NABar/1.0',
    'Mozilla/5.0 (Linux; Android 9; Redmi Note 7 Pro Build/PKQ1.181203.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/76.0.3809.89 Mobile Safari/537.36 T7/11.21 SP-engine/2.17.0 baiduboxapp/11.21.0.10 (Baidu; P1 9)',
    'Mozilla/5.0 (Linux; Android 10; LYA-TL00 Build/HUAWEILYA-TL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/76.0.3809.89 Mobile Safari/537.36 T7/11.21 SP-engine/2.17.0 baiduboxapp/11.21.0.10 (Baidu; P1 10)',
    'Mozilla/5.0 (Linux; Android 10; BLA-AL00 Build/HUAWEIBLA-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/76.0.3809.89 Mobile Safari/537.36 T7/11.21 SP-engine/2.17.0 baiduboxapp/11.21.0.10 (Baidu; P1 10)',
    'Mozilla/5.0 (Linux; Android 9; FLA-AL10 Build/HUAWEIFLA-AL10; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/76.0.3809.89 Mobile Safari/537.36 T7/11.21 SP-engine/2.17.0 baiduboxapp/11.21.0.10 (Baidu; P1 9)',
    'Mozilla/5.0 (Linux; U; Android 10; zh-cn; SEA-AL10 Build/HUAWEISEA-AL10) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/66.0.3359.126 MQQBrowser/10.2 Mobile Safari/537.36'
]

screenInfo = [
    "2048*1152*60",
    "1920*1080*60",
    "1920*1080*30",
    "2048*3072*30",
    "2048*3072*60",
    "1920*1200*60",
    "1920*1200*30"
]

dingtalk_proxy = {"proxy": 'http://mlj:mlj@127.0.0.1:9001'}