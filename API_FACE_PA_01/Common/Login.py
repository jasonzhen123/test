# -*- coding:utf-8 -*-
from Common import dirConfig
import requests
import json

#登录
host = dirConfig.host
def login():
    url = host+"/login"
    headers={"Accept": "application/json, text/javascript, */*; q=0.01",
             "Accept-Encoding": "gzip, deflate",
             "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
             "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0",
             "X-Requested-With": "XMLHttpRequest",
             "Content-Type": "application/json; charset=utf-8",
             "Connection": "keep-alive",
             "Referer": "http://192.168.1.115:8088/login",
             "Host": "192.168.1.115:8088"
             }
    body = {"loginName":dirConfig.loginName,"pwd":dirConfig.pwd}
    s = requests.session()
    res = s.post(url,json=body,headers=headers,verify=False,files=None)
    return s
print(login())
if __name__ == "__main__":
    a = login(username='admin',pwd='e10adc3949ba59abbe56e057f20f883e')
