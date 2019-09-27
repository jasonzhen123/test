# -*- coding:utf-8 -*-

import HTMLTestRunnerCN_test1
import unittest
import time
import yaml
from Common import dirConfig
from Common import myLogger2

testCase_path = dirConfig.testCase_path
def createSuite1():
    testUnit=unittest.TestSuite()
    discover=unittest.defaultTestLoader.discover(testCase_path,pattern='test_*.py',top_level_dir=None)
    for test_suite in discover:
        #print(test_suite)
        for test_case in test_suite:
            testUnit.addTest(test_case)
            print(testUnit)
    return testUnit

curTime = time.strftime("%Y-%m-%d %H_%M_%S",time.localtime())
fp = open(dirConfig.htmlReport_dir + '/API_autoTest_{0}.html'.format(curTime), 'wb')

runner=HTMLTestRunnerCN_test1.HTMLTestRunner(
    stream=fp,
    title=u'FACE自动化接口测试报告',
    description=u'用例执行情况：')

runner.run(createSuite1())

#关闭文件流，不关的话生成的报告是空的
fp.close()
