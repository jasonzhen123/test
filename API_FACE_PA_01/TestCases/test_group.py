# -*- coding:utf-8 -*-
from Common import Post_Get
from Common import MyFunction
import random
import json
import unittest


'''
测试思路：只有在增删改差，基本都类似，不赘述，只列出字段及含义
前提条件：需要角色roleId,

1./sysManage/group/add   增加用户组
2./sysManage/group/qry   查询角色
3./sysManage/group/edit  编辑角色
4./sysManage/group/del   删除角色
'''

global_vars = {}

class TestGroup(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.result = Post_Get
        #创建角色返回roleId、返回priId
        name = random.randint(100,1000)
        roleData = MyFunction.create_role(name)
        global_vars["roleId"] = roleData["roleId"]
        global_vars["priId"] = roleData["priId"]

    @classmethod
    def tearDownClass(cls):
        #删除角色及权限
        uri = "/sysManage/role/del"
        body = {"ids":global_vars["roleId"]}
        res = Post_Get.post(uri,body)

        uri = "/sysManage/privilege/del"
        body = {"ids":global_vars["priId"]}
        res = Post_Get.post(uri,body)

    def test_01_add(self):
        num = random.randint(100,1000)
        name = "测试{0}".format(num)

        uri = "/sysManage/group/add"
        body = {
                  "enName": "",
                  "name": name,
                  "remark": "string",
                  "roleId": global_vars["roleId"]
        }
        res = self.result.post(uri,body)
        dict = json.loads(res.content)
        code = dict["code"]
        self.assertEqual(code,0)

        global_vars["name"] = name

    def test_02_qry(self):
        uri = "/sysManage/group/qry?enName=&name={0}&pageNo=1&pageSize=10".format(global_vars["name"])
        res = self.result.get(uri)
        dict = json.loads(res.content)
        code = dict["code"]
        self.assertEqual(code,0)
        #取出id值，添加为全局变量
        id = dict["data"]["records"][0]["id"]
        global_vars["id"] = id

    def test_03_edit(self):
        uri = "/sysManage/group/edit"
        body = {
                  "enName": "",
                  "id": global_vars["id"],
                  "name": global_vars["name"],
                  "remark": "",
                  "roleId": global_vars["roleId"]
        }
        res = self.result.post(uri,body)
        dict = json.loads(res.content)
        code = dict["code"]
        self.assertEqual(code,0)

    def test_04_del(self):
        uri = "/sysManage/group/del"
        body = {"ids":global_vars["id"]}
        res = self.result.post(uri,body)
        dict = json.loads(res.content)
        code = dict["code"]
        self.assertEqual(code,0)