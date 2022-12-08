<!--
 * @Descripttion: 
 * @version: 
-->
# spider

##编译+打包
python3 setup.py build && python3 setup.py bdist_wheel

##编译+打包+重装
python3 setup.py build && python3 setup.py bdist_wheel && pip uninstall spider && pip install dist/spider-#.#.#-py3-none-any.whl

#### 安装教程   
本模块为内部使用模块，不进行线上发布，可直接通过./dist/目录获取最新的版本（版本号最大）,直接通过命令安装:   

pip3/pip3 install spider-#.#.#-py3-none-any.whl

#### 最新稳定版路径  
##### ./stable/spider-*.*.*-py3-none-any.whl

#### 功能说明  



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
