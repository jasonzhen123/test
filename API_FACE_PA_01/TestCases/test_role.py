# -*- coding:utf-8 -*-
from Common import Post_Get
from Common import MyFunction
import random
import json
import unittest
import time
import requests

'''
测试思路：只有在增删改差，基本都类似，不赘述，只列出字段及含义
1./sysManage/role/add   增加角色
2./sysManage/role/edit  编辑角色
3./sysManage/role/qry   查询角色
4./sysManage/role/del   删除角色
'''

global_vars = {}

class TestRole(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.result = Post_Get
        #创建一个权限，返回权限的id、name,,为创建角色使用
        name = random.randint(100,1000)
        priData = MyFunction.create_privilege(name)
        global_vars["priId"] = priData["priId"]
        global_vars["priName"] = priData["priName"]

    @classmethod
    def tearDownClass(cls):
        cls.result1 = Post_Get
        uri_del = "/sysManage/privilege/del"
        body_del = {"ids": global_vars["priId"],
                    "userId": ""}
        res1 = cls.result1.post(uri_del,body_del)

    def test_01_add(self):
        num = random.randint(100,1000)
        name = "测试{0}".format(num)
        uri = "/sysManage/role/add"
        body = {"name":name,
                "enName":"",
                "priId":global_vars["priId"]}
        time.sleep(1)
        res = self.result.post(uri,body)
        dict = json.loads(res.content)
        code = dict["code"]
        self.assertEqual(code,0)
        global_vars["name"] = name

    def test_02_qry(self):
        uri = "/sysManage/role/qry?enName=&name={0}&pageNo=1&pageSize=10".format(global_vars["name"])
        res = self.result.get(uri)
        #print(res.text)
        dict = json.loads(res.content)
        code = dict["code"]
        self.assertEqual(code,0)
        id = dict["data"]["records"][0]["id"]
        global_vars["id"] = id

    def test_03_edit(self):
        uri = "/sysManage/role/edit"
        body = {
                 "enName": "",
                 "id": global_vars["id"],
                 "name": "001测试",
                "priId": global_vars["priId"],
                "priName":global_vars["priName"],
                "remark": ""}
        res = self.result.post(uri,body)
        dict = json.loads(res.content)
        code = dict["code"]
        self.assertEqual(code,0)

    def test_04_del(self):
        uri = "/sysManage/role/del"
        body = {"ids":global_vars["id"]}
        res = self.result.post(uri,body)
        dict = json.loads(res.content)
        code = dict["code"]
        self.assertEqual(code,0)