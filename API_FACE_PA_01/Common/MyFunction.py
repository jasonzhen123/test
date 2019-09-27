# -*- coding:utf-8 -*-
from Common import Login
from Common import dirConfig
import random
import time
import json
import base64
import requests

#post请求
def post(uri,body=None):
    ses = Login.login()
    url = dirConfig.host+uri
    res = ses.post(url,json=body,verify=False)
    return res

#get请求
def get(uri):
    ses = Login.login()
    url = dirConfig.host+uri
    res = ses.get(url,verify=False)
    return res

#输入路径输出图片的base64数据
def get_base64(pictFile):
    pict_file = open(pictFile,'rb')
    pict_base64 = base64.b64encode(pict_file.read())
    #将bytes类型转化为str类型
    pict_base64 = pict_base64.decode("utf-8")
    pict_file.close()
    return pict_base64

#输入人像库名称，创建并返回人像id
def create_faceGroup(num):
    #创建人像库
    regData = {}
    uri_add='/faceGroup/add'
    name = "测试{0}".format(num)
    body_add = {"name":name,"extInfo":""}
    res = post(uri_add,body_add)
    #通过增加的人像库的name,获取对应的id,
    time.sleep(1)
    uri_qry = '/faceGroup/get?extInfo=&name={0}'.format(name )
    res = get(uri_qry)
    dict = json.loads(res.content)
    regId = dict["content"]["getRegistLib"]["records"][0]["id"]
    regName = dict["content"]["getRegistLib"]["records"][0]["name"]
    regData["regId"] = regId
    regData["regName"] = regName
    return regData

#输入权限，创建并返回权限id
def create_privilege(num):
    priData = {}
    #创建一个权限，返回权限的id
    name = "测试{0}".format(num)
    uri_add='/sysManage/privilege/add'
    body_add = {"enName": "",
                "name": name,
                "remark": ""}
    res1 = post(uri_add,body_add)
    #通过增加的权限name,获取对应的id,创建人，创建时间
    uri_qry = '/sysManage/privilege/qry?name={0}&pageNo=1&pageSize=10'.format(name)
    res = get(uri_qry)
    dict = json.loads(res.content)
    priId = dict["data"]["records"][0]["id"]
    #priName = dict["data"]["records"][0]["name"]
    priData["priName"] = name
    priData["priId"] = priId
    return priData

#输入角色，创建并返角色id,权限Id
def create_role(num):
    roleData ={}
    #先创建权限,创建的权限也要删除掉，如何实现？
    num_pri = random.randint(100,1000)
    priData = create_privilege(num_pri)
    roleData["priId"] = priData["priId"]
    roleData["priName"] = priData["priName"]

    name = "测试{0}".format(num)
    uri = "/sysManage/role/add"
    body = {"name":name,
            "enName":"",
            "priId":priData["priId"] }

    res = post(uri,body)
    #通过角色name查询角色id
    uri_1 = "/sysManage/role/qry?enName=&name={0}&pageNo=1&pageSize=10".format(name)
    res = get(uri_1)
    dict = json.loads(res.content)
    #取出id值，添加为全局变量
    roleId = dict["data"]["records"][0]["id"]
    roleData["roleId"] = roleId
    roleData["roleName"] = name
    return roleData

#创建角色,返回groupId、roleId、priId
def create_group(num):
    groData = {}
    role_num = random.randint(100,1000)
    roleData = create_role(role_num)
    groData["roleId"] = roleData["roleId"]
    groData["priId"] = roleData["priId"]
    #输入num,创建用户组，返回Id
    group_name = "测试{0}".format(num)
    uri = "/sysManage/group/add"
    body = {
              "enName": "",
              "name": group_name,
              "remark": "string",
              "roleId": groData["roleId"]
    }
    res = post(uri,body)
    uri = "/sysManage/group/qry?enName=&name={0}&pageNo=1&pageSize=10".format(group_name)
    res = get(uri)
    dict = json.loads(res.content)
    groupId = dict["data"]["records"][0]["id"]
    groData["groupId"] = groupId
    return groData

#创建机构返回机构id
def create_organization(num):
    orgData = {}
    name = "测试{0}".format(num)
    uri_add='/sysManage/organization/add'
    body_add = {
                "address": "",
                "code": num,
                "contactPerson": "",
                "name": name,
                "remark": "",
                "telephone": "" }
    res1 = post(uri_add,body_add)

    uri_qry = '/sysManage/organization/qry?name={0}&pageNo=1&pageSize=10'.format(name)
    res = get(uri_qry)
    dict = json.loads(res.content)
    orgId = dict["data"]["records"][0]["id"]
    orgData["orgId"] = orgId
    orgData["orgName"] = name
    return orgData

#创建部门返回，部门id、机构id
def create_department(num):
    dptData = {}
    num1 = random.randint(100,1000)
    orgData = create_organization(num1)
    dptData["orgId"] = orgData["orgId"]
    dptData["orgName"] = orgData["orgName"]
    #传入num,创建部门
    name = "测试{0}".format(num)
    uri_add='/sysManage/department/add'
    body_add = {
                "address": "",
                "code": num,
                "contactPerson": "",
                "name": name,
                "remark": "",
                "telephone": "",
                "orgId":orgData["orgId"]
                }
    res = post(uri_add,body_add)
    #通过增加的部门name,获取对应的id,创建人，创建时间
    uri_qry = '/sysManage/department/qry?name={0}&pageNo=1&pageSize=10'.format(name)
    res = get(uri_qry)
    dict = json.loads(res.content)
    dptId = dict["data"]["records"][0]["id"]
    dptData["dptId"] = dptId
    dptData["dptName"] = name
    return dptData

#创建相机返回相机id
def create_camera(num):
    cameraData = {}
    name = "测试{0}".format(num)
    num1 = random.randint(10,1000)
    uri = "192.168.2.{0}".format(num1)
    uri_add = "/camera/add"
    body = {"name":name,"status":"","areaCode":"54956819","unitCode":"","cameraType":"1",
            "threshold":"","sluiceChannel":1,"follwarea":"","deptCode":"undefined",
            "analyseServerCode":"undefined","vasServerCode":"undefined","uri":uri,
            "userName":"admin","password":"123456"}
    res1 = post(uri_add,body)
    dict1 = json.loads(res1.content)
    cameraData["cameraId"] = dict1["data"]
    cameraData["cameraName"] = name
    cameraData["cameraUrl"] = uri
    return cameraData

#创建布控，返回布控id、相机id、人像库id
#调用布控管理时，会创建相机机人像库，调用完成需要将相机跟人像库删除保持环境干净
def create_surveillance(num):
    surData = {}
    #创建相机返回cameraId
    cam_num = random.randint(100,1000)
    cameraData = create_camera(cam_num)
    surData["cameraId"] = cameraData["cameraId"]
    surData["cameraName"] = cameraData["cameraName"]

    #创建人像库返回regId
    reg_num = random.randint(100,1000)
    regData = create_faceGroup(reg_num)
    surData["regId"] = regData["regId"]
    surData["regName"] = regData["regName"]

    name = "测试{0}".format(num)
    uri = "/surveillance/add"
    body = {
              "cameraId": surData["cameraId"],
              "cameraName": surData["cameraName"],
              "controlStatus": 1,
              "controlTimeType": "A",#布控时间类型用ABCD表示？
              "controlType": 1,
              #"endTime": "",#创建布控信息的时间加上默认一个月的时间，就是布控结束时间
              "name": name,
              "regId": surData["regId"],
              "regName": surData["regName"],
              "remark": "",
             #"startTime": "",
              "threshold": 50,
              #"userId": 1,
    }
    res = post(uri,body)
    dict = json.loads(res.content)
    surId = dict["content"]["createAlarmLib"]
    surData["surId"] = surId
    surData["surName"] = name
    return surData

#创建顶级的行政中心返回区域id
def create_area(num):
    dataArea = {}
    name = "测试{0}".format(num)
    uri = "/sysManage/area/add"
    body = {"id":"","name":name,"parentId":"","parentName":"","remark":""}
    res = post(uri,body)
    time.sleep(1)
    uri_qry = "/sysManage/area/qry?pageNo=1&pageSize=999&name={0}".format(name)
    res_get = get(uri_qry)
    dict = json.loads(res_get.content)
    parentId = dict["data"]["records"][0]["id"]
    parentName = dict["data"]["records"][0]["name"]

    dataArea["parentId"] = parentId
    dataArea["parentName"] = parentName
    return dataArea
