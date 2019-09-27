# -*- coding:utf-8 -*-
from Common import Post_Get
import random
import json
import unittest
import time
import requests

'''
人像库信息管理测试思路：
1.add   增加一个人像库(名字随机获取)，获取返回数据进行断言，同时通过机构名称获取机构对应的id等信息；
2.update    通过新增人像库的id，进行编辑操作后，获取返回数据进行断言；
3.get   通过查询人像库信息，获取返回数据进行断言；
4.getFaceNumber 通过人像库id，查询该人像库信息，获取返回数据进行断言；
5.delete    通过id将新增的人像库进行删除。

'''
global_vars = {}

class TestFaceGroup(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.result = Post_Get

    #测试增加人像库
    def test_01_add(self):
        num = random.randint(100,1000)
        name = "测试{0}".format(num)
        uri_add='/faceGroup/add'

        body_add = {"name":name,"extInfo":""}
        #增加人像库请求及结果断言
        res = self.result.post(uri_add,body_add)
        self.assertEqual(res.status_code,200)

        #通过增加的人像库的name,获取对应的id,
        time.sleep(1)
        uri_qry = '/faceGroup/get?extInfo=&name={0}'.format(name)
        res = self.result.get(uri_qry)
        dict = json.loads(res.content)
        id = dict["content"]["getRegistLib"]["records"][0]["id"]
        global_vars["key_id"] = id
        global_vars["key_name"] = name

    #测试更新人像库
    def test_02_update(self):
        #uri、body参数
        uri = '/faceGroup/update?extInfo=&id={}&name={}'.format(global_vars["key_id"],global_vars["key_name"])
        body = {}
        res = self.result.post(uri,body)
        self.assertEqual(res.status_code,200)

    #测试通过id查询人像库
    def test_03_getFaceNumber(self):
        #uri参数
        uri = "/faceGroup/getFaceNumber?id={0}".format(global_vars["key_id"])
        res = self.result.get(uri)
        dict = json.loads(res.content)
        #获取records数据进行比对
        records_value = dict["result"]["retDesc"]
        self.assertEqual(records_value,records_value)

    #测试查询所有人像库
    def test_04_get(self):
        uri = "/faceGroup/get"
        res = self.result.get(uri)
        dict = json.loads(res.content)
        records_value = dict["content"]["getRegistLib"]["records"][0]
        self.assertIsNotNone(records_value)

    #测试删除机构
    def test_05_del(self):
        #uri、body参数
        uri_del = "http://192.168.1.115:8088/faceGroup/delete"
        res1 = requests.post(uri_del,global_vars["key_id"])
        dict1 = json.loads(res1.content)
        code = dict1["result"]["retCode"]

        self.assertEqual(code,"00")
