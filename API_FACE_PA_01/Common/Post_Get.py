# -*- coding:utf-8 -*-
from Common import Login

import random
import json
import requests

global_vars = {}
#post请求，传入uri_add,body

def post(uri,body=None):
    #body1 = json.dumps(body)
    ses = Login.login()
    url = "http://192.168.1.115:8088"+uri

    res = ses.post(url,json=body,verify=False)
    return res

#get请求，传入uri_add,body
def get(uri):
    ses = Login.login()
    url = "http://192.168.1.115:8088"+uri
    res = ses.get(url,verify=False)
    return res



uri= ''
# res = get(uri_qry)
# print(res.text)