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
首选创建一个顶级行政中心，已经在MyFunction创建直接调用就OK
1./sysManage/area/add   增加区域
2./sysManage/area/qry  查询区域
3./sysManage/area/edit   编辑区域
4./sysManage/area/del   删除区域
'''

global_vars = {}

class TestRole(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.result = Post_Get
        #创建顶级行政中心,并返回parentId、parentName
        name = random.randint(100,1000)
        dataArea = MyFunction.create_area(name)

        global_vars["parentId"] = dataArea["parentId"]
        global_vars["parentName"] = dataArea["parentName"]

    @classmethod
    def tearDownClass(cls):
        cls.result1 = Post_Get
        uri_del = "/sysManage/area/del"
        body_del = {"ids": global_vars["parentId"]}
        res = cls.result1.post(uri_del,body_del)

    def test_01_add(self):
        num = random.randint(100,1000)
        name = "测试{0}".format(num)
        uri = "/sysManage/area/add"
        body = {"id":"","name":name,"parentId":global_vars["parentId"],
                "parentName":global_vars["parentName"],"remark":""}

        res = self.result.post(uri,body)
        dict = json.loads(res.content)
        code = dict["code"]
        self.assertEqual(code,0)

        global_vars["name"] = name

    def test_02_qry(self):
        uri = "/sysManage/area/qry?enName=&name={0}&pageNo=1&pageSize=10".format(global_vars["name"])
        res = self.result.get(uri)
        #print(res.text)
        dict = json.loads(res.content)
        code = dict["code"]
        self.assertEqual(code,0)
        #取出id值，添加为全局变量
        id = dict["data"]["records"][0]["id"]
        global_vars["id"] = id

    def test_03_edit(self):
        name = random.randint(100,1000)
        uri = "/sysManage/area/edit"
        body = {"id": global_vars["id"],
                "name": name,
                "parentId": global_vars["parentId"],
                "parentName":global_vars["parentName"],
                "remark": ""}
        res = self.result.post(uri,body)
        dict = json.loads(res.content)
        code = dict["code"]
        self.assertEqual(code,0)

    def test_04_del(self):
        uri = "/sysManage/area/del"
        body = {"ids":global_vars["id"]}
        res = self.result.post(uri,body)
        dict = json.loads(res.content)
        code = dict["code"]
        self.assertEqual(code,0)
