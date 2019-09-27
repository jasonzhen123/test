
import os

common_dir = os.path.split(os.path.abspath(__file__))[0]

testCase_dir = common_dir.replace("Common","TestDatas")

htmlReport_dir =common_dir.replace("Common","HtmlTestReport")

htmlReport_dir1 =common_dir.replace("Common","HtmlTestReport1")

testDate_dir = common_dir.replace("Common","TestDatas")

logs_dir = common_dir.replace("Common","Logs")

#ip地址
host = "http://192.168.1.114:8088"
#用户名及密码
loginName= "admin"
pwd = "e10adc3949ba59abbe56e057f20f883e"
#图片1路径
pict1_path = "G:\\01WorkSpace(Pycharm)\\API_FACE_PA\\Common\\1.jpg"
#图片2路径
pict2_path = "G:\\01WorkSpace(Pycharm)\\API_FACE_PA\\Common\\2.jpg"
#压缩文件路径
fileUp_path = "G:\\01WorkSpace(Pycharm)\\API_FACE_PA\\Common\\face_test_100.zip"
#测试用例文件路径
testCase_path = "G:\\01WorkSpace(Pycharm)\\API_FACE_PA\\TestCases"
#测试数据excel名字
testData_excelName = "/api_info_1.xlsx"
