# main.py首部添加
import pytest
import os
# Fix for Python >= 3.10 compatibility
import sys
from collections.abc import Sequence
import collections
collections.Sequence = Sequence


if sys.version_info >= (3, 10):
    collections.Mapping = collections.abc.Mapping
    collections.MutableMapping = collections.abc.MutableMapping
    # Add other ABCs as needed

if __name__ == '__main__':
    # 1.执行测试用例
    pytest.main()
    # os.system("copy environment.properties  .\\report")
    # 2.生成报告
    # os.system("allure generate report -o allure-report --clean")
    # # 3.打开报告
    # os.system("allure open allure-report")
