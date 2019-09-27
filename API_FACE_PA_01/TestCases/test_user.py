# -*- coding:utf-8 -*-
from Common import Post_Get
from Common import MyFunction
import random
import unittest
import json
import requests

#目前用户接口不通
'''
测试思路：只有在增删改差，基本都类似，不赘述，只列出字段及含义
前提条件：
创建用户组返回groupId,创建部门返回dptId
清理操作：
删除所创建的部门及用户组
1./sysManage/user/add 增加角色
2./sysManage/user/qry 查询角色
3./sysManage/user/userpri 获取用户菜单权限
4./sysManage/user/editCamera 修改用户相机权限,要获取相机的pri
5./sysManage/user/editHuman 修改用户人像库权限,要先获取相机的pri
6./sysManage/user/reset 密码重置
7./sysManage/user/edit  编辑角色
9./sysManage/user/del   删除角色
'''

global_vars = {}

class TestUser(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.result = Post_Get
        #创建用户组返回用户组、角色、权限Id
        group_num = random.randint(100,1000)
        group_name = "测试{0}".format(group_num)
        groData= MyFunction.create_group(group_name)
        #将groData里面的用户组、角色、权限Id设置为全局变量，最后清除掉
        global_vars["groupId"] = groData["groupId"]
        global_vars["roleId"] = groData["roleId"]
        global_vars["priId"] = groData["priId"]

        #创建部门返回部门Id、组织Id
        dpt_num = random.randint(100,1000)
        dptData= MyFunction.create_department(dpt_num)
        global_vars["dptId"] = dptData["dptId"]
        global_vars["orgId"] = dptData["orgId"]

        #创建人像库
        faceGroup_num = random.randint(100,1000)
        faceGroup_name = "测试{0}".format(faceGroup_num)
        regData = MyFunction.create_faceGroup(faceGroup_name)
        global_vars["regId"] = regData["regId"]

        #创建相机
        camera_num = random.randint(100,1000)
        cameraData = MyFunction.create_camera(camera_num)
        global_vars["cameraId"] = cameraData["cameraId"]

    @classmethod
    def tearDownClass(cls):
        #删除创建的用户组
        uri = "/sysManage/group/del"
        body = {"ids":global_vars["groupId"]}
        res = Post_Get.post(uri,body)
        #删除角色
        uri = "/sysManage/role/del"
        body = {"ids":global_vars["id"]}
        res = Post_Get.post(uri,body)
        #删除创建的权限
        uri_del = "/sysManage/privilege/del"
        body_del = {"ids": global_vars["priId"],
                    "userId": ""}
        res1 = Post_Get.post(uri_del,body_del)
        #删除创建的部门
        uri_del = "/sysManage/department/del"
        body_del = {"ids": global_vars["dptId"],
                    "userId": ""}
        res = Post_Get.post(uri_del,body_del)
        #删除创建的组织
        uri_del = "/sysManage/organization/del"
        body_del = {"ids": global_vars["orgId"],
                    "userId": ""}
        res = Post_Get.post(uri_del,body_del)
        #删除创建的相机
        uri = "/camera/delete"
        body = {"ids":global_vars["cameraId"]}
        res = Post_Get.post(uri,body)
        #删除创建的人像库
        uri_del = "http://192.168.1.115:8088/faceGroup/delete"
        res1 = requests.post(uri_del,global_vars["regId"])

    def test_01_add(self):
        num = random.randint(100,1000)
        name = "测试{0}".format(num)
        telNum = random.randint(10000000000,1000000000000)

        uri = "/sysManage/user/add"
        body = {"groupId":global_vars["groupId"],
                "dptId":global_vars["dptId"],
                "name":name,
                "tel":telNum,
                "realName":name,
                "passwd":"{0}".format(telNum),
                "email":"{0}@qq.com".format(telNum)
                }
        res = self.result.post(uri,body)
        dict = json.loads(res.content)
        code = dict["code"]
        self.assertEqual(code,0)
        global_vars["name"] = name
        global_vars["telNum"] = telNum

    def test_02_qry(self):
        uri = "/sysManage/user/qry?name={0}&pageNo=1&pageSize=999&realName=".format(global_vars["name"])
        res = self.result.get(uri)
        #print(res.text)
        dict = json.loads(res.content)
        code = dict["code"]
        self.assertEqual(code,0)
        #取出id值，添加为全局变量
        id = dict["data"]["records"][0]["id"]
        global_vars["id"] = id
    '''
    def test_03_chPwd(self):
        uri = "/sysManage/user/chPwd"
        body = {
                  "newPwd": "123456",
                  "oldPwd": "{0}".format(global_vars["telNum"])
        }
        res = self.result.post(uri,body)
        print(body)
        dict = json.loads(res.content)
        code = dict["code"]
        self.assertEqual(code,0)
        '''
    def test_04_userPri(self):
        uri = "/sysManage/user/userpri"
        res = self.result.get(uri)
        #print(res.text)
        dict = json.loads(res.content)
        code = dict["code"]
        self.assertEqual(code,0)

    def test_05_edit(self):
        num = random.randint(100,1000)
        name = "测试{0}".format(num)
        uri = "/sysManage/user/edit"

        body = {"name":"name",
                "groupId":global_vars["groupId"],
                "realName":global_vars["name"],
                "tel":global_vars["telNum"],
                "dptId":global_vars["dptId"],
                "email":"{0}@qq.com".format(global_vars["telNum"]),
                "remark":"",
                "id":global_vars["id"],
                "passwd":""}

        res = self.result.post(uri,body)
        dict = json.loads(res.content)
        code = dict["code"]
        self.assertEqual(code,0)

    def test_06_editCamera(self):
        uri = "/sysManage/user/editCamera"
        body = {
                  "id":  global_vars["id"],
                  "pri": global_vars["cameraId"]
                }
        res = self.result.post(uri,body)
        dict = json.loads(res.content)
        code = dict["code"]
        self.assertEqual(code,0)

    def test_07_editHuman(self):
        uri = "/sysManage/user/editHuman"
        body =  {
                  "id":  global_vars["id"],
                  "pri": global_vars["regId"]
                }
        res = self.result.post(uri,body)
        dict = json.loads(res.content)
        code = dict["code"]
        self.assertEqual(code,0)

    def test_08_reset(self):
        uri = "/sysManage/user/reset?id={0}".format(global_vars["id"])
        res = self.result.get(uri)
        #print(res.text)
        dict = json.loads(res.content)
        code = dict["code"]
        self.assertEqual(code,0)

    def test_09_delete(self):
        uri = "/sysManage/user/del"
        body = {"ids":global_vars["id"]}
        res = self.result.post(uri,body)
        dict = json.loads(res.content)
        code = dict["code"]
        self.assertEqual(code,0)