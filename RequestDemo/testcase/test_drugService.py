import pytest
from util.request_util import HttpClient
from util.logger import Logger
from jsonschema import validate
import allure
from util.assertcompare import assert_compare

logger=Logger().logger
client = HttpClient()



# 响应数据校验Schema
RESPONSE_SCHEMA = {
    "type": "object",
    "required": ["resultCode", "result", "msg"],
    "properties": {
        "resultCode": {"type": "number", "enum": [0, 400]},
        "result": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["commonName", "spec", "price"],
                "properties": {
                    "commonName": {"type": "string", "pattern": "^[\u4e00-\u9fa5a-zA-Z0-9]+$"},
                    "spec": {"type": "string", "minLength": 1},
                    "price": {"type": "number", "minimum": 0}
                }
            }
        },
        "msg": {"type": "string"}
    }
}
class TestUserAPI:
    @allure.story("验证模糊查询")
    @pytest.mark.parametrize("case", pytest.api_test_data)
    def test_api_requests(self, case):
        logger.info(f"执行用例 %s "% case['name'])
        # 发送请求并获取响应
        response = client.post(
        endpoint = case["request"]["url"],
        data = case["request"]["headers"],
        json = case["request"]["body"]
        )
        response_data = response.json()
        # 第一层：基础HTTP验证
        # assert response.status_code == case['expect']['status_code']
        assert response.status_code == 200
        # # 第二层：JSON Schema验证
        # response_data = response.json()
        # validate(instance=response_data, schema=RESPONSE_SCHEMA)
        # 第三层：关键字断言
        if 'response_contains' in case['expect']:
            assert case['expect']['response_contains'] in response_data
        if case["name"] == "药品搜索-正常流测试":
            assert any(
                item["commonName"] == "特非那定片"
                and "60毫克" in item["spec"]
                for item in response_data["result"])
  # 第三层：业务逻辑验证
        if case["name"] == "药品搜索-正常流测试":
            for item in response_data["result"]:
                assert_compare (item["chainSellId"] == case['expect']['chainSellId'])
                assert_compare (item["spec"] == case['expect']['spec'])

