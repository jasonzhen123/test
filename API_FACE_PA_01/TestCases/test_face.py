# -*- coding:utf-8 -*-
from Common import Post_Get
from Common import MyFunction
from Common import dirConfig
import random
import json
import unittest
import time
import requests

'''
权限管理各接口的整体思路：
setUpClass：要先将一张图片转化为base64,需要创建两个人像库，一个用于导入人像信息，一个用于人像信息的移动跟复制
tearDownClass:
1.add   先增加一条人像信息，获取返回数据进行断言code,并获取addPersionToLib；
2.update  修改人像信息后，断言；
3.updateBodyImage   修改图片信息后，断言；
4.shear  移动人像信息，断言；
5.copy   获取id,ids进行断言；
6.fileUpload    压缩文件请求如何发送；
7.batchExprot   文件路径及人像库regid;
8.get    通过输入前面人像库的regId,查询导入的人像信息，断言；
9.delete   通过ids号,将所有的人像信息进行删除。
'''

global_vars = {}

class TestFace(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.result = Post_Get
        #将common目录下的图片转化为base64；
        data1_base64 = MyFunction.get_base64(dirConfig.pict1_path)
        global_vars["data1_base64"] = data1_base64

        #导入人像需要人像库，创建人像库1,返回人像库的regId_01；
        num_1 = random.randint(100,1000)
        regData_01 = MyFunction.create_faceGroup(num_1)
        global_vars["regId01"] = regData_01["regId"]

        #导入人像需要人像库，创建人像库2,返回人像库的regId_02；
        num_2 = random.randint(100,1000)
        regData_02 = MyFunction.create_faceGroup(num_2)
        global_vars["regId02"] = regData_02["regId"]

        #导入人像需要人像库，创建人像库3,返回人像库的regId_03；
        num_3 = random.randint(100,1000)
        regData_03 = MyFunction.create_faceGroup(num_3)
        global_vars["regId03"] = regData_03["regId"]

    @classmethod
    def tearDownClass(cls):
        #将初始条件当中创建的两个人像库删除掉
        uri_del = "{0}/faceGroup/delete".format(dirConfig.host)
        res1 = requests.post(uri_del,global_vars["regId01"])
        res2 = requests.post(uri_del,global_vars["regId02"])
        res3 = requests.post(uri_del,global_vars["regId03"])

    #测试导入人像
    def test_01_add(self):
        num = random.randint(100,1000)
        name = "测试{0}".format(num)
        uri_add='/face/add'

        body_add = {"regId": global_vars["regId01"],
                    "name": name,
                    "sex" :"1",
                    "age" :"20",
                    "image": global_vars["data1_base64"]
                    }
        #增加权限请求及结果断言
        res1 = self.result.post(uri_add,body_add)
        dict1 = json.loads(res1.content)
        code = dict1["result"]["retCode"]
        self.assertEqual(code,"00")
        #获取该人像的addPersionToLib
        addPersionToLib = dict1["content"]["addPersionToLib"]
        global_vars["addPersionToLib"] = addPersionToLib
        global_vars["name"] = name

    def test_02_fileUpload(self):
        url = '{0}/face/fileUpload'.format(dirConfig.host)
        files = {"data":open(dirConfig.fileUp_path, "rb")}
        res = requests.post(url,files=files)
        dict = json.loads(res.content)
        code = dict["code"]
        self.assertEqual(code,0)
        data_filePath = dict["data"]
        global_vars["data_filePath"] = data_filePath

    def test_03_batchExprot(self):
        uri = '/face/batchExport?regId={0}&uploadPath={1}'.format(global_vars["regId02"],global_vars["data_filePath"])
        res = self.result.post(uri)
        dict = json.loads(res.content)
        code = dict["code"]
        self.assertEqual(code,0)

    #测试更新人像信息
    def test_04_update(self):
        #uri、body参数
        uri = '/face/update'
        body = {"id":global_vars["addPersionToLib"],
                "age" :"20",
                "name":global_vars["name"],
                "regId":global_vars["regId01"],
                "sex" :"1"
                }
        #编辑权限请求及结果断言
        res = Post_Get.post(uri,body)
        dict = json.loads(res.content)
        code = dict["result"]["retCode"]
        self.assertEqual(code,"00")

    #测试人像在移动
    def test_05_shear(self):
        #获取当前人像信息id,获取要移动到的人像库的regId
        uri = '/face/shear?id={0}&regId={1}'.format(global_vars["addPersionToLib"],global_vars["regId02"])
        time.sleep(1)
        res = self.result.post(uri)
        dict = json.loads(res.content)
        code = dict["result"]["retCode"]
        self.assertEqual(code,"00")

    #测试人像复制
    def test_06_copy(self):
        #获取当前人像信息id,获取要复制到的人像库的regId
        uri = '/face/copy?id={0}&regId={1}'.format(global_vars["addPersionToLib"],global_vars["regId03"])
        time.sleep(1)
        res = self.result.post(uri)
        dict = json.loads(res.content)
        code = dict["result"]["retCode"]
        self.assertEqual(code,"00")

    #测试更新人像图片
    def test_07_updateBodyImage(self):
        #获取另一个要更新的人像图片的base64
        data2_base64 = MyFunction.get_base64(dirConfig.pict2_path)
        uri = '/face/updateBodyImage'
        body = {
                "Image": data2_base64,
                "id": global_vars["addPersionToLib"],
                "age":"",
                "identifyNumber":"",
                "name":global_vars["name"],
                "regId":global_vars["regId03"],
                "sex":"1",
                "remark": ""
                }
        #编辑权限请求及结果断言
        time.sleep(1)
        res = self.result.post(uri,body)
        dict1 = json.loads(res.content)
        code = dict1["result"]["retCode"]
        self.assertEqual(code,"00")

    #测试查询人像信息
    def test_08_get(self):
        uri = "/face/get"
        res = self.result.get(uri)
        dict = json.loads(res.content)
        records_value = dict["content"]["getPersons"]["records"][0]["id"]
        #print(records_value)
        self.assertIsNotNone(records_value)

    def test_09_delet(self):
        uri_del = "/face/delete"
        body_del = {"ids": global_vars["addPersionToLib"]
                    }
        res1 = self.result.post(uri_del,body_del)
        dict1 = json.loads(res1.content)
        code = dict1["result"]["retCode"]
        self.assertEqual(code,"00")