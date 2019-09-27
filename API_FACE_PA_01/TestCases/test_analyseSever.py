# -*- coding:utf-8 -*-
from Common import Post_Get
import random
import json
import unittest
import time
import requests

'''
抓拍服务器管理接口测试思路：
前提条件：需要部门id、需要创建一个用户名及密码、需要抓拍服务器的ip地址及端口
1./resource/analyseServer/add 增加
2./resource/analyseServer/get 查询
3./resource/analyseServer/getServerStatus 服务器连接测试
4./resource/analyseServer/getSlaveStatus 查询抓拍服务器状态
5./resource/analyseServer/update 修改
6./resource/analyseServer/delete
'''