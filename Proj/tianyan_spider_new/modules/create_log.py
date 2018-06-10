import logging
import os
from logging.handlers import TimedRotatingFileHandler


def creat_log(log_path='/home/changzuxian/tianyancha', level=logging.INFO):
    """
    创建app的日志handle
    :param: 日志路径:
    :return: 日志logger
    """
    LOGGING_MSG_FORMAT = '[%(asctime)s] [%(filename)s[line:%(lineno)d]] [%(levelname)s] [%(message)s]'
    LOGGING_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
    logging.basicConfig(level=level, format=LOGGING_MSG_FORMAT, datefmt=LOGGING_DATE_FORMAT)
    if not os.path.exists(log_path):
        os.makedirs(log_path)
    LOG_PATH = os.path.join(log_path, "tianyancha2.log")
    fileHandler = logging.handlers.WatchedFileHandler(LOG_PATH)
    fileHandler.setFormatter(logging.Formatter(LOGGING_MSG_FORMAT))
    logger = logging.getLogger()
    logger.addHandler(fileHandler)
    return logger
