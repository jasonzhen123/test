# -*- coding:utf-8 -*-
from Common import Post_Get
import random
import json
import unittest
'''
权限管理各接口的整体思路：
1.add   先增加一条权限(随机获取)，获取返回数据进行断言；
2.edit  通过新增权限的名称得到ID号，进行编辑操作，进行修改操作后，获取返回数据进行断言；
3.menu  查询权限菜单列表，获取返回数据进行断言，对返回数据进行处理；
4.pri   拿到第三步的权限数据，对该权限设置菜单权限，获取返回数据，进行断言；
5.getpri    通过ID号，获取该ID号对应的权限，获取返回数据，断言；
6.del   通过ids号,进行权限删除；
7.qry   进行权限查询，获取返回结果，进行断言。
'''

global_vars = {}

class TestPrivilege(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.result = Post_Get

    #测试增加权限
    def test_01_add(self):
        num = random.randint(100,1000)
        name = "测试{0}".format(num)
        uri_add='/sysManage/privilege/add'

        body_add = {"enName": "",
                    "name": name,
                    "remark": ""}
        #增加权限请求及结果断言
        res1 = self.result.post(uri_add,body_add)
        dict1 = json.loads(res1.content)
        code = dict1["code"]
        self.assertEqual(code,0)
        #通过增加的权限name,获取对应的id,创建人，创建时间
        uri_qry = '/sysManage/privilege/qry?name={0}&pageNo=1&pageSize=10'.format(name)
        res = self.result.get(uri_qry)
        dict = json.loads(res.content)
        id = dict["data"]["records"][0]["id"]
        createPerson = dict["data"]["records"][0]["createPerson"]
        createTime = dict["data"]["records"][0]["createTime"]
        global_vars["key_id"] = id
        global_vars["key_creatPerson"] = createPerson
        global_vars["key_createTime"] = createTime
        global_vars["key_name"] = name

    #测试编辑权限
    def test_02_edit(self):
        #uri、body参数
        uri_edit = '/sysManage/privilege/edit'
        body_edit = {"createPerson": global_vars["key_creatPerson"],
                     "createTime": global_vars["key_createTime"],
                     "enName": "admin",
                     "id": global_vars["key_id"],
                     "name": global_vars["key_name"],
                     "remark": ""}
        #编辑权限请求及结果断言
        res1 = self.result.post(uri_edit,body_edit)
        dict1 = json.loads(res1.content)
        code = dict1["code"]
        self.assertEqual(code,0)

    #测试查询菜单
    def test_03_menu(self):
        uri_menu = "/sysManage/privilege/menu"
        res = self.result.get(uri_menu)
        dict = json.loads(res.content)
        #获取records数据进行比对
        records_value = dict["data"]["records"][0]
        self.assertIsNotNone(records_value)

    #测试设置菜单权限
    def test_04_pri(self):
        uri_pri = "/sysManage/privilege/pri"
        body_pri = {"ids": "9,10,11,12,13,14,29,30,20,21,22,23,24,25,26,27,28",
                     "priId": global_vars["key_id"]}
        res1 = self.result.post(uri_pri,body_pri)
        dict1 = json.loads(res1.content)
        code = dict1["code"]
        self.assertEqual(code,0)

    #测试菜单权限查询
    def test_05_getpri(self):
        #id = "1544779050145"
        uri_getpri = "/sysManage/privilege/getpri?id={0}".format(global_vars["key_id"])
        res1 = self.result.get(uri_getpri)
        dict1 = json.loads(res1.content)
        code = dict1["code"]
        self.assertEqual(code,0)

    #测试删除权限
    def test_06_del(self):
        uri_del = "/sysManage/privilege/del"
        body_del = {"ids": global_vars["key_id"],
                    "userId": ""}
        res1 = self.result.post(uri_del,body_del)
        dict1 = json.loads(res1.content)
        code = dict1["code"]
        self.assertEqual(code,0)
    #测试权限查询
    def test_07_qry(self):
        uri_qry = "/sysManage/privilege/qry"
        res1 = self.result.get(uri_qry)
        dict1 = json.loads(res1.content)
        code = dict1["code"]
        self.assertEqual(code,0)