from datetime import datetime

import requests
import allure
from typing import Optional, Union, Dict, Any
from util.logger import Logger

logger=Logger().logger

class HttpClient:
    '''
    endpoint: str：强制要求传入字符串类型的API端点路径
    params: Optional[Dict]：可选字典参数，用于GET请求的查询参数（会拼接到URL后）
    ** kwargs：可变关键字参数，可传递所有requests支持的底层参数 ,透传其他所有参数（如headers/timeout等）'''

    def __init__(self, base_url: str = ""):
        self.session = requests.Session()
        self.base_url = base_url

    def _log_request(self, method: str, url: str, **kwargs):
        logger.info(f"准备请求: {method} {url}")
        logger.debug(f"请求参数: {kwargs.get('params', '无')}")
        if 'json' in kwargs:
            logger.debug(f"请求JSON: {kwargs['json']}")
        if 'data' in kwargs:
            logger.debug(f"表单数据: {kwargs['data']}")

    def _log_response(self, resp: requests.Response):
        logger.debug(f"收到响应: {resp.status_code} {resp.reason}")
        logger.debug(f"响应头: {resp.headers}")
        logger.debug(f"响应内容: {resp.text[:500]}...")  # 截断长内容

    @allure.step("发送GET请求")
    def get(self, endpoint: str, params: Optional[Dict] = None, **kwargs) -> requests.Response:
        return self._request("GET", endpoint, params=params, **kwargs)

    @allure.step("发送POST请求")
    def post(self, endpoint: str, data: Optional[Union[Dict, str]] = None,
             json: Optional[Dict] = None, **kwargs) -> requests.Response:
        return self._request("POST", endpoint, data=data, json=json, **kwargs)

    @allure.step("发送PUT请求")
    def put(self, endpoint: str, data: Optional[Union[Dict, str]] = None, **kwargs) -> requests.Response:
        return self._request("PUT", endpoint, data=data, **kwargs)

    @allure.step("发送DELETE请求")
    def delete(self, endpoint: str, **kwargs) -> requests.Response:
        return self._request("DELETE", endpoint, **kwargs)

    def _attach_response_details(self, resp: requests.Response):
        """将响应详情附加到对象属性（供后续使用）"""
        self.last_response = {
            'status_code': resp.status_code,
            'headers': dict(resp.headers),
            'content': resp.text[:1000]  # 保留部分内容供调试
        }

    def _handle_error(self, exception: Exception, url: str):
        """统一错误处理"""
        error_info = {
            'url': url,
            'error_type': type(exception).__name__,
            'timestamp': datetime.now().isoformat()
        }
        logger.error(f"错误详情: {error_info}")

    def _request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        url = f"{self.base_url}{endpoint}"
        self._log_request(method, url, **kwargs)

        try:
            resp = self.session.request(method, url, **kwargs)
            self._log_response(resp)
            self._attach_response_details(resp)
            resp.raise_for_status()
            return resp
        except requests.exceptions.RequestException as e:
            logger.error(f"请求异常: {str(e)}", exc_info=True)
            self._handle_error(e, url)
            raise
        except Exception as e:
            logger.critical(f"未知异常: {str(e)}", exc_info=True)
            raise
