# -*- coding:utf-8 -*-

from Common import Post_Get
from Common import MyFunction
import random
import unittest
import datetime
import json
'''
测试思路：
前置条件：创建一条正常日志
1./sysManage/log/exportData 日志导出详情
2./sysManage/log/qry 日志查询
'''

global_vars = {}

class TestGroup(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        start_time = datetime.datetime.now()
        #创建权限增加日志
        name = random.randint(100,1000)
        priData = MyFunction.create_privilege(name)
        global_vars["priId"] = priData["priId"]
        #删除创建的权限
        uri_del = "/sysManage/privilege/del"
        body_del = {"ids": global_vars["priId"],
                    "userId": ""}
        res1 = Post_Get.post(uri_del,body_del)
        end_time = datetime.datetime.now()
        #print(end_time)
        global_vars["start_time"] = start_time
        global_vars["end_time"] = end_time

    def test_01_qry(self):
        uri = "/sysManage/log/qry?module=&name=&pageNo=&description={0}&pageSize=&status=&time{1}=&type=&userName=".format("权限删除",global_vars["start_time"])
        res = Post_Get.get(uri)
        dict = json.loads(res.content)
        records = dict["data"]["records"][0]
        self.assertIsNotNone(records)
        #print(res.content)

    def test_02_exportData(self):
        uri = "/sysManage/log/qry?logType=&module=&name=&pageNo=1&pageSize=10&status=&time=&type=&userName="
        res = Post_Get.get(uri)
        dict = json.loads(res.content)
        records = dict["data"]["records"][0]
        self.assertIsNotNone(records)