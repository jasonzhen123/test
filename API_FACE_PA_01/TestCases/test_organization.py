# -*- coding:utf-8 -*-
from Common import Post_Get
import random
import json
import unittest

'''
机构管理测试思路：
1.add   增加一个机构(名字随机获取)，获取返回数据进行断言，同时通过机构名称获取机构对应的id等信息；
2.edit  通过新增机构的名称得到ID号，进行编辑操作，进行修改操作后，获取返回数据进行断言；
3.qry   拿到第二步的机构对应的id号，然后通过查询接口查询到这个id对应的信息，取出返回数据中的id，进行断言；
4.del   通过id号,进行权限删除。
'''

global_vars = {}

class TestOrganization(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.result = Post_Get

    #测试增加机构
    def test_01_add(self):
        #num = random.randint(100,1000)
        num = 1011
        uri_add='/sysManage/organization/add'
        body_add = {
                    "address": "",
                    "code": num,
                    "contactPerson": "",
                    "name": num,
                    "remark": "",
                    "telephone": ""
}
        #增加机构请求及结果断言
        res = self.result.post(uri_add,body_add)
        dict = json.loads(res.content)
        code = dict["code"]
        self.assertEqual(code,0)

        #通过增加的机构name,获取对应的id,创建人，创建时间
        uri_qry = '/sysManage/organization/qry?name={0}&pageNo=1&pageSize=10'.format(num)
        res = self.result.get(uri_qry)
        dict = json.loads(res.content)
        id = dict["data"]["records"][0]["id"]
        global_vars["key_num"] = num
        global_vars["key_id"] = id
        #print(res.text)

    #测试编辑机构
    def test_02_edit(self):
        #uri、body参数
        uri_edit = '/sysManage/organization/edit'
        body_edit = {"name":global_vars["key_num"],
                     "code":global_vars["key_num"],
                     "address":"",
                     "contactPerson":"",
                     "telephone":"",
                     "remark":"",
                     "id":global_vars["key_id"],
                    "checked":"true"}
        res = self.result.post(uri_edit,body_edit)
        dict = json.loads(res.content)
        code = dict["code"]
        self.assertEqual(code,0)

    #测试查询机构
    def test_03_qry(self):
        #uri参数
        uri_menu = "/sysManage/organization/qry?id={0}&pageNo=1&pageSize=10".format(global_vars["key_id"])
        res = self.result.get(uri_menu)
        dict = json.loads(res.content)
        #获取records数据进行比对
        records_value = dict["data"]["records"][0]["id"]
        self.assertEqual(records_value,global_vars["key_id"])

    #测试删除机构
    def test_04_del(self):
        #uri、body参数
        uri_del = "/sysManage/organization/del"
        body_del = {"ids": global_vars["key_id"],
                    "userId": ""}
        res = self.result.post(uri_del,body_del)
        dict = json.loads(res.content)
        code = dict["code"]
        self.assertEqual(code,0)
        print(res.text)