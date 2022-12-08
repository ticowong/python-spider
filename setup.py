'''
Descripttion: 
version: 
Author: tico.wong
Date: 2022-12-08
LastEditors: tico.wong
'''

from setuptools import find_packages
from distutils.core import setup

install_requires = [
    'pymysql==0.9.3',
    'requests==2.24.0',
    'aiohttp==3.7.3',
    'DBUtils==2.0',
    'aioredis==1.3.1',
    'aiomysql==0.0.21',
    'redis==3.2.1',
    'protobuf==3.20.1',
    'aliyun-log-python-sdk==0.7.11',
    'wheel==0.37.1',
    'kafka-python==2.0.2',
]

excluded = ('spider.gitignore',)

setup(
    name='python-spider',
    version='1.0.0',
    author='tico.wong',
    author_email='ticowong@163.com',
    url='https://github.com/ticowong',
    description='personal python spider frame',
    packages=find_packages(),
    install_requires=install_requires,
    license='BSD License',
    include_package_data=True,
    classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Natural Language :: Chinese (Simplified)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Software Development :: Libraries'
    ],
    package_data={
        '': ['*.txt', '*.gz'],
        'bandwidth_reporter': ['*.txt', '*.gz']
    },
)
