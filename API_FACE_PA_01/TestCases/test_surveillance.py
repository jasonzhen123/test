# -*- coding:utf-8 -*-
from Common import Post_Get
from Common import MyFunction
from Common import dirConfig
import random
import json
import unittest
import requests
import time

'''
布控信息管理测试思路：
setUpClass:创建相机返回cameraId、cameraName,
           创建人像库名称返回regId、regName
tearDownClass:删除所创建的相机、人像库
1.add   增加布控，返回进行断言，返回结果可以获取布控编号；
2.qry   可以通过新增布控的名称，查询该布控的信息，返回结果进行断言；
3.control
4.getSurvellanceType
5.update
6.edit  通过新增机构的名称得到ID号，进行编辑操作，进行修改操作后，获取返回数据进行断言；
7.del   通过id号,进行权限删除。
'''

global_vars = {}

class TestSurveillance(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.result = Post_Get
        #创建相机
        cam_num = random.randint(100,1000)
        cameraData = MyFunction.create_camera(cam_num)
        global_vars["cameraId"] = cameraData["cameraId"]
        global_vars["cameraName"] = cameraData["cameraName"]
        #创建人像库
        reg_num = random.randint(100,1000)
        regData = MyFunction.create_faceGroup(reg_num)
        global_vars["regId"] = regData["regId"]
        global_vars["regName"] = regData["regName"]

    @classmethod
    def tearDownClass(cls):
        #删除创建的相机、人像库
        uri = "/camera/delete"
        body = {"ids":global_vars["cameraId"]}
        res = Post_Get.post(uri,body)
        uri_del = "{0}/faceGroup/delete".format(dirConfig.host)
        res1 = requests.post(uri_del,global_vars["regId"])

    def test_01_add(self):
        num = random.randint(100,1000)
        name = "测试{0}".format(num)
        uri = "/surveillance/add"
        body = {
                  "cameraId": global_vars["cameraId"],
                  "cameraName": global_vars["cameraName"],
                  "controlStatus": 1,
                  "controlTimeType": "A",#布控时间类型用ABCD表示？
                  "controlType": 1,
                  #"endTime": "",#创建布控信息的时间加上默认一个月的时间，就是布控结束时间
                  "name": name,
                  "regId": global_vars["regId"],
                  "regName": global_vars["regName"],
                  "remark": "",
                 #"startTime": "",
                  "threshold": 50,
                  #"userId": 1,
        }
        res = self.result.post(uri,body)
        dict = json.loads(res.content)
        code = dict["result"]["retCode"]
        self.assertEqual(code,"00")
        id = dict["content"]["createAlarmLib"]
        global_vars["id"] = id
        global_vars["name"] = name
        print(global_vars["regId"])
        print(global_vars["regName"])
        print(global_vars["cameraId"])
        print(global_vars["cameraName"])

    def test_02_get(self):
        uri = "/surveillance/get?name={0}".format(global_vars["name"])
        res = self.result.get(uri)
        dict = json.loads(res.content)
        records_value = dict["content"]["getAlarmInfoLib"]["records"][0]
        self.assertIsNotNone(records_value)

    def test_03_control(self):
        #status=1表示停用，=2表示启用
        uri = "/surveillance/control?id={0}&status=1".format(global_vars["id"])
        res = self.result.get(uri)
        dict = json.loads(res.content)
        code = dict["result"]["retCode"]
        self.assertEqual(code,"00")

    def test_04_getSurvellanceType(self):
        uri = "/surveillance/getSurvellanceType?survellanceType=1"
        res = self.result.get(uri)
        dict = json.loads(res.content)
        code = dict["code"]
        self.assertEqual(code,0)
    '''
    def test_05_update(self):
        cameraName = 123
        ad = json.dumps(cameraName)
        #ad = cameraName.decode("utf-8")
        uri = "/surveillance/update"
        body = {
                  "cameraId": global_vars["cameraId"],
                  "cameraName": str(1),
                  "controlStatus": 1,
                  "controlTimeType": "A",#布控时间类型用ABCD表示？
                  "controlType": 1,
                  #"endTime": "",#创建布控信息的时间加上默认一个月的时间，就是布控结束时间
                  "id": global_vars["id"],
                  "name": global_vars["name"],
                  "regId": global_vars["regId"],
                  "regName": global_vars["regName"],
                  "remark": "",
                 #"startTime": "",
                  "threshold": 100,
                  "vasServerChannel":"80",
                  #"userId": 1,
        }
        print(body)
        res = self.result.post(uri,body)
        dict = json.loads(res.content)
        print(res.text)
        code = dict["result"]["retCode"]
        #将00转化为unicode格式，否则无法跟获得的retCode进行比对
        #code_00 = "00".encode("utf-8")
        self.assertEqual(code,"00")
    '''
    def test_06_delete(self):
        uri = "/surveillance/delete"
        body = {"ids":global_vars["id"],"userId":1}
        res1 = self.result.post(uri,body)
        dict1 = json.loads(res1.content)
        code = dict1["result"]["retCode"]
        self.assertEqual(code,"00")


