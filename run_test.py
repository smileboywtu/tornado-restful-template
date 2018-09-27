# -*- coding: utf-8 -*-

"""

加载测试用例并测试

:create: 2018/9/23
:copyright: smileboywtu

"""

import sys
import time
import unittest
from io import StringIO
from unittest import TextTestRunner


def load_tests(dir_name):
    """
    从文件夹中加载测试用例
    
    :param dir_name: 文件夹名字
    :return: 
    """
    return unittest.TestLoader().discover(dir_name)


class TestRunner():
    def __init__(self):
        self.all_suite = unittest.TestSuite()
        self.output = StringIO()
        self.all_results = None
        self.start_time = time.time()
        self.wasSuccessful = 1

    def init_suite(self):
        """
        添加测试用例到测试套件中
        :return: 
        """
        self.all_suite.addTests(load_tests("common"))
        self.all_suite.addTests(load_tests("application"))


    def run_suite(self, test_suite):
        self.all_results = TextTestRunner(stream=self.output,
                                          verbosity=1).run(test_suite)
        self.wasSuccessful = 0 if self.all_results.wasSuccessful() else 1
        print("测试失败: ", self.all_results.failures)
        print("测试错误: ", self.all_results.errors)
        print("测试结果: %s" % "通过" if self.wasSuccessful == 0 else "失败", self.all_results)

    def run_all_suite(self):
        self.init_suite()
        self.run_suite(self.all_suite)


if __name__ == "__main__":
    test_runner = TestRunner()
    test_runner.run_all_suite()
    result = test_runner.wasSuccessful
    sys.exit(result)
