import os
import time
import logging
from logging.handlers import RotatingFileHandler
from util.get_filepath  import get_log_path


class Logger:
    def __init__(self):
        logpath = get_log_path()
        os.makedirs(logpath, exist_ok=True)

        self.logger = logging.getLogger('app')
        if not self.logger.handlers:
            self.logger.setLevel(logging.DEBUG)
            formatter = logging.Formatter(
                '[%(asctime)s][%(process)d:%(thread)d][%(filename)s:%(lineno)d][%(levelname)s]: %(message)s'
            )

            # 文件Handler（自动切割）
            file_handler = RotatingFileHandler(
                filename=os.path.join(logpath, f"{time.strftime('%Y-%m-%d')}.log"),
                maxBytes=10 * 1024 * 1024,
                backupCount=5,
                encoding='utf-8'
            )
            file_handler.setFormatter(formatter)

            # 控制台Handler
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)

            self.logger.addHandler(file_handler)
            self.logger.addHandler(console_handler)

    def __del__(self):
        for handler in self.logger.handlers:
            handler.close()


def get_logger():
    return Logger().logger


if __name__ == '__main__':
    logger = get_logger()
    logger.info("测试INFO日志")
    logger.debug("测试DEBUG日志")
