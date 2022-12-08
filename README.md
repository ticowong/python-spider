<!--
 * @Descripttion: 
 * @version: 
 * @Author: afcentry
 * @Date: 2021-05-21 17:09:39
 * @LastEditors: afcentry
 * @LastEditTime: 2022-09-17 13:49:25
-->
# CommonPart

##编译+打包
python3 setup.py build && python3 setup.py bdist_wheel

##编译+打包+重装
python3 setup.py build && python3 setup.py bdist_wheel && pip uninstall CommonPart && pip install dist/CommonPart-#.#.#-py3-none-any.whl

#### 安装教程   
本模块为内部使用模块，不进行线上发布，可直接通过./dist/目录获取最新的版本（版本号最大）,直接通过命令安装:   

pip3/pip3 install CommonPart-#.#.#-py3-none-any.whl

#### 最新稳定版路径  
##### ./stable/CommonPart-*.*.*-py3-none-any.whl

#### 功能说明  

1.  模块名称设置  
    本方法对当前程序进行名称设计，主要对与在进行网络请求是需要用到代理的程序进行代理使用时使用情况统计区分的作用。  
    ```python
    from CommonPart.combuiltin.combuiltin import  CommonVar
    CommonVar.model_name = 'name'  #  不设置则默认为default
    ```
2.  获取当前系统时间  
    from CommonPart.combuiltin.combuiltin import  ComBuiltin  
    current_time = ComBuiltin.get_current_time()  
    结果示例：2022-01-01 13:30:00  
3.  获取档期日期  
    from CommonPart.combuiltin.combuiltin import  ComBuiltin  
    current_time = ComBuiltin.get_current_date()  
    结果示例：2022-01-01  
4.  获取13位时间戳  
    from CommonPart.combuiltin.combuiltin import  ComBuiltin  
    timestamp13 = ComBuiltin.get_timestamp13()    
5.  发起get网络请求(post请求相似)  
    from CommonPart.combuiltin.combuiltin import  ComBuiltin  
    resppnse = ComBuiltin.get()  #参数均与requests格式保持一致  
    自定义参数:  
    (1) trytimes: 若本次请求发起失败，则需要进行重拾的次数  
    (2) ifproxy: 本次请求是否使用代理IP,True/False(使用代理IP的前提首先需对本程序进行全局设置是否支持代理请求,设置方式:  
        from CommonPart.combuiltin.combuiltin import  CommonVar
        CommonVar.global_proxy = True/False  #  不设置则默认为default 
        )
    结果示例：ClientResponse  
6.  异步发起get网络请求(post请求相似)  
    ```python
    from CommonPart.combuiltin.combuiltin import  ComBuiltin  
    return_info = await ComBuiltin.async_get()  #参数均与requests格式保持一致      
    return_info['text'] = soup  # 页面源码
    return_info['url'] = url
    return_info['headers'] = headers
    return_info['status'] = status
    return_info['cookies'] = cookies
    return_info['history'] = history  
    ```
7.  异步操作mysql  
    ```python
    from CommonPart.kernel.dbnode import AsyncMysqlUtils  
    dbconfig = {
        'host': 'host',
        'port': 3306,
        'db': 'product',
        'user': 'product',
        'password': 'password',
        'charset': 'utf8mb4',
        'autocommit': True # 执行自动提交，无需commit
    }
    local_product = AsyncMysqlUtils()
    aiwait local_product.init_pool(**dbconfig)
    """
    查询:local_product.select(sql)
    增、删、改:status = local_product.execute(sql)
    """
    ```
8.  调用内建函数获取淘宝商品数字ID-仅支持异步调用   
    from CommonPart.tkutils.tb import query_item_id_by_sign    
    item_id = await query_item_id_by_sign(sign_id=sign_id)

#### 参与贡献 1

1.  Fork 本仓库
2.  新建 Feat_xxx 分支
3.  提交代码
4.  新建 Pull Request


#### 特技

1.  使用 Readme\_XXX.md 来支持不同的语言，例如 Readme\_en.md, Readme\_zh.md
2.  Gitee 官方博客 [blog.gitee.com](https://blog.gitee.com)
3.  你可以 [https://gitee.com/explore](https://gitee.com/explore) 这个地址来了解 Gitee 上的优秀开源项目
4.  [GVP](https://gitee.com/gvp) 全称是 Gitee 最有价值开源项目，是综合评定出的优秀开源项目
5.  Gitee 官方提供的使用手册 [https://gitee.com/help](https://gitee.com/help)
6.  Gitee 封面人物是一档用来展示 Gitee 会员风采的栏目 [https://gitee.com/gitee-stars/](https://gitee.com/gitee-stars/)
