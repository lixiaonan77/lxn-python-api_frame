'''import pytest
import os
if __name__ == "__main__":
    # 1.运行用例，生成Allure原始数据
    pytest.main([
        "testcase/",
        "-v",
        "--alluredir=./allure-results",#报告数据目录
        ])
    #2.自动打开Allure报告(Windows/Linux/Mac通用)
    os.system("allure generate ./allure-results -o ./allure-report --clean")
    os.system("allure open ./allure-report")
   '''

import pytest
import os

if __name__ == "__main__":
    # 1. 运行用例，生成 Allure 原始数据
    pytest.main([
        "testcase/",
        "-v",
        "--alluredir=./allure-results",  # 报告数据目录
    ])

    # 2. 自动打开 Allure 报告（Windows/Linux/Mac 通用）
    os.system("allure generate ./allure-results -o ./allure-report --clean")
    os.system("allure open ./allure-report")
