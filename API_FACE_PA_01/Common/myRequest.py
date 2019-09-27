#Author:小豪

import requests
import ast

def myRequest(url,method,request_data):
    #1.判断是get还是post请求
    #2.调用request相应的方法、url、请求数据
    #3.获取返回值
    #判断数据是否为空，不为空则转换成字典类型的数据
    if request_data is not None:
        request_data = ast.literal_eval(request_data)

    if method == "get":
        res = requests.get(url,request_data)
    elif method == "post":
        res = requests.post(url,json=request_data)
    else:
        res = None
    return res