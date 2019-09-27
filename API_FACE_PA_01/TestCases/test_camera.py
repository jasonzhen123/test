# -*- coding:utf-8 -*-

from Common import Post_Get
import random
import json
import unittest
import time
import requests


'''
测试相机信息的思路：
1.add   先增加一个相机，获取返回数据进行断言code,并获取addPersionToLib
2.control   相机启动控制
3.get   查询相机信息
4.getCameraSnapshot 获取相机流快照
5.getCameraTree 监控点相机树
6.getCameraTreeByCameraName 监控点(相机)树按相机名称查询
7.update    修改相机信息
8.delete    删除相机信息
'''

global_vars = {}

class TestCamera(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.result = Post_Get

    def test_01_add(self):
        num_1 = random.randint(1000,10000)
        name = "测试{0}".format(num_1)
        num_2 = random.randint(100,1000)
        uri = "192.168.1.{0}".format(num_2)

        uri_add = "/camera/add"
        body = {"name":name,"status":"","areaCode":"54956819","unitCode":"","cameraType":"1",
                "threshold":"","sluiceChannel":1,"follwarea":"","deptCode":"undefined",
                "analyseServerCode":"undefined","vasServerCode":"undefined","uri":uri,
                "userName":"admin","password":"123456"}

        time.sleep(3)
        res= self.result.post(uri_add,body)
        print(res.text)
        dict = json.loads(res.content)
        code = dict["code"]
        self.assertEqual(code,0)
        global_vars["id"] = dict["data"]
        global_vars["uri"] = uri
        global_vars["name"] = name

    def test_02_control(self):
        uri = "/camera/control?cameraType=1&id={0}&isvalid=2".format(global_vars["id"])
        time.sleep(1)
        res = self.result.post(uri)
        dict = json.loads(res.content)
        code = dict["code"]
        self.assertEqual(code,0)

    def test_03_get(self):
        uri = "/camera/get"
        res = self.result.get(uri)
        dict = json.loads(res.content)
        records_value = dict["records"][0]
        self.assertIsNotNone(records_value)

    def test_04_getCameraSnapshot(self):
        uri = "/camera/getCameraSnapshot?cameraUrl={0}".format(global_vars["uri"])

        res = self.result.get(uri)
        dict = json.loads(res.content)
        #print res.content
        code = dict["code"]
        self.assertEqual(code,0)

    def test_05_getCameraTreeByCameraName(self):
        uri = "/camera/getCameraTree?cameraType=1"
        res = self.result.get(uri)
        dict = json.loads(res.content)
        records_value = dict[0]
        self.assertIsNotNone(records_value)

    def test_06_update(self):
        uri = "/camera/update"
        body = {"id":global_vars["id"],"cameraType":"1","name":global_vars["name"],"status":"",
                "isvalid":1,"unitCode":"","areaCode":"54956819","deptCode":"undefined","snapIp":global_vars["uri"],
                "snapPort":"","userName":"admin","uri":global_vars["uri"],"password":"123456","externalCode":"",
                "analyseServerCode":"undefined","installAddress":"","longitude":"0","latitude":"0",
                "threshold":"",
                "sluiceChannel":"1","follwarea":"","vasServerCode":"undefined","vasServerChannel":"",
                "orientationType":""}
        res = self.result.post(uri,body)
        dict = json.loads(res.content)
        code = dict["code"]
        self.assertEqual(code,0)

    # def test_07_delete(self):
    #     uri = "/camera/delete"
    #     body = {"ids":global_vars["id"]}
    #     res = self.result.post(uri,body)
    #     dict = json.loads(res.content)
    #     code = dict["code"]
    #     self.assertEqual(code,0)

