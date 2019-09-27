# -*- coding:utf-8 -*-
from Common import Post_Get
from Common import dirConfig
import unittest
import requests
import json
from Common import Login
'''
测试思路：
1.login 登录
2.logout 登出
3./sessionTimeOut 查询是否超时
'''
global_vars = {}

class TestFace(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.result = Post_Get

    def test_01_login(self):
        uri = "{0}/login".format(dirConfig.host)
        body = {"loginName":dirConfig.loginName,"pwd":dirConfig.pwd}

        res = requests.post(uri,json=body)
        #res1 = requests.post(uri,json=body)

        dict1 = json.loads(res.content)
        code = dict1["code"]
        self.assertEqual(code,0)
        global_vars["cookiesData"] = res.cookies.get_dict()

    def test_02_sessionTimeOut(self):
        #取出cookie，加入headers当中
        headers = {"cookie" : "JSESSIONID={0}".format(global_vars["cookiesData"]["JSESSIONID"])}
        uri = "{0}/sessionTimeOut".format(dirConfig.host)
        res = requests.get(uri,headers= headers)
        dict = json.loads(res.content)
        code = dict["code"]
        self.assertEqual(code,0)

    def test_03_logout(self):
        uri = "/logout"
        res = self.result.get(uri)
        dict = json.loads(res.content)
        code = dict["code"]
        self.assertEqual(code,0)
