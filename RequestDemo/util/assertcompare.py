from util.logger import Logger
from typing import Any, Union

logger=Logger().logger

_COMPARE_OPERATORS = {
    "==": lambda x, y: x == y,
    "!=": lambda x, y: x != y,
    ">": lambda x, y: x > y,
    "<": lambda x, y: x < y,
    ">=": lambda x, y: x >= y,
    "<=": lambda x, y: x <= y,
    "in": lambda x, y: x in y,
    "not in": lambda x, y: x not in y,
    "is": lambda x, y: x is y,
    "is not": lambda x, y: x is not y
}


def assert_compare(
        expect: Any,
        compare: str,
        actual: Any,
        extra_msg: str = ""
) -> None:
    """增强型断言比较工具

    Args:
        expect: 预期值
        compare: 比较运算符(支持==,!=,>,<,>=,<=,in,not in,is,is not)
        actual: 实际值
        extra_msg: 附加的调试信息

    Raises:
        ValueError: 当比较符不合法时
        AssertionError: 当断言失败时
    """
    logger.info(f"Assert: {expect!r} {compare} {actual!r} {extra_msg}")

    if compare not in _COMPARE_OPERATORS:
        error_msg = f"非法比较符: {compare}, 可用: {list(_COMPARE_OPERATORS.keys())}"
        logger.error(error_msg)
        raise ValueError(error_msg)

    try:
        if not _COMPARE_OPERATORS[compare](expect, actual):
            error_msg = (
                f"断言失败: {expect!r} {compare} {actual!r}\n"
                f"类型: expect={type(expect)}, actual={type(actual)}"
            )
            logger.error(error_msg)
            raise AssertionError(error_msg)
        logger.info("断言通过")
    except Exception as ex:
        logger.error(f"比较过程异常: {str(ex)}", exc_info=True)
        raise
