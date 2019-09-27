# -*- coding:utf-8 -*-
from Common import Post_Get
from Common import MyFunction
import random
import json
import unittest

'''
机构管理测试思路：
前提条件：要先创建一个机构，
结束处理：将创建的机构进行删除
1.add   增加一个部门(名字随机获取)，获取返回数据进行断言，同时通过部门名称获取机构对应的id等信息；
2.edit  通过新增部门的名称得到ID号，进行编辑操作，进行修改操作后，获取返回数据进行断言；
3.qry   拿到第二步的部门对应的id号，然后通过查询接口查询到这个id对应的信息，取出返回数据中的id，进行断言；
4.del   通过id号,进行部门删除。
'''

global_vars = {}

class TestDepartment(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.result = Post_Get
        #先创建一个机构，通过机构名称，获取机构id、name,即部门的orgId、orgName,设置为全局变量
        num = random.randint(100,1000)
        orgData = MyFunction.create_organization(num)

        global_vars["key_orgId"] = orgData["orgId"]
        global_vars["key_orgName"] = orgData["orgName"]

    @classmethod
    def tearDownClass(cls):
        cls.result1 = Post_Get
        #将之前创建的机构删除
        #uri、body参数
        uri_del = "/sysManage/organization/del"
        body_del = {"ids": global_vars["key_orgId"],
                    "userId": ""}
        res = cls.result1.post(uri_del,body_del)

    #测试增加部门
    def test_01_add(self):
        num = random.randint(100,1000)
        uri_add='/sysManage/department/add'

        body_add = {
                    "address": "",
                    "code": num,
                    "contactPerson": "",
                    "name": num,
                    "remark": "",
                    "telephone": "",
                    "orgId":global_vars["key_orgId"]
}
        res = self.result.post(uri_add,body_add)
        dict = json.loads(res.content)
        code = dict["code"]
        self.assertEqual(code,0)

        #通过增加的部门name,获取对应的id,创建人，创建时间
        uri_qry = '/sysManage/department/qry?name={0}&pageNo=1&pageSize=10'.format(num)
        res = self.result.get(uri_qry)
        dict = json.loads(res.content)
        id = dict["data"]["records"][0]["id"]
        global_vars["key_num"] = num
        global_vars["key_id"] = id

    #测试编辑部门
    def test_02_edit(self):
        #uri、body参数
        uri_edit = '/sysManage/department/edit'
        body_edit = {"name":global_vars["key_num"],
                     "orgId":global_vars["key_orgId"],
                     "contactPerson":"",
                     "telephone":"",
                     "remark":"",
                     "id":global_vars["key_id"],
                    "orgName":global_vars["key_orgName"]}

        res = self.result.post(uri_edit,body_edit)
        dict = json.loads(res.content)
        code = dict["code"]
        self.assertEqual(code,0)

    #测试查询部门
    def test_03_qry(self):
        #uri参数
        uri_menu = "/sysManage/department/qry?id={0}&pageNo=1&pageSize=10".format(global_vars["key_id"])
        res = self.result.get(uri_menu)
        dict = json.loads(res.content)
        #获取records数据进行比对
        records_value = dict["data"]["records"][0]["id"]
        self.assertEqual(records_value,global_vars["key_id"])
        #self.assertIsNotNone(records_value)

    #测试删除部门
    def test_04_del(self):
        #uri、body参数
        uri_del = "/sysManage/department/del"
        body_del = {"ids": global_vars["key_id"],
                    "userId": ""}

        res = self.result.post(uri_del,body_del)
        dict = json.loads(res.content)
        code = dict["code"]
        self.assertEqual(code,0)