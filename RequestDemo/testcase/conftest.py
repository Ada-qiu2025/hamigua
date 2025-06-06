import pytest
import yaml
from util.get_filepath import get_yaml_path

def load_search_data():
    data_file = get_yaml_path()
    with open(data_file, encoding='utf-8') as f:
        data = yaml.safe_load(f)
        if isinstance(data, list):  # 兼容旧版列表结构
            return {"test_cases": data}
        return data


def pytest_configure(config):
    # 加载YAML数据并注册为全局变量
    pytest.api_test_data = load_search_data()["test_cases"]

@pytest.fixture(scope="module")
def search_test_data():
    """提供药品搜索测试数据集"""
    yield load_search_data()

@pytest.fixture
def search_case(request, search_test_data):
    """动态获取单个测试用例"""
    case_name = request.param
    return next(c for c in search_test_data if c["name"] == case_name)

