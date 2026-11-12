import logging
import os
from datetime import datetime
from typing import NoReturn

from colorlog import ColoredFormatter

from src.utils.singleton import SingletonMeta


class Logger(metaclass=SingletonMeta):
    LOG_FORMAT_FOR_CMD = '%(log_color)s %(levelname)s:  %(log_color)s%(message)s%(reset)s'
    LOG_FORMAT_FOR_FILE = '%(asctime)s [%(levelname)s]: %(message)s'

    _logger: logging.Logger = None
    _file_handler: logging.FileHandler = None
    _stream_handler: logging.StreamHandler = None

    @classmethod
    def _get_logger(cls, output_dir=os.getcwd()) -> logging.Logger:
        if cls._logger is None:
            cls._logger = logging.getLogger('autotests') 
            cls._logger.setLevel(logging.INFO)
            cls._logger.propagate = False

            cls._stream_handler = logging.StreamHandler()
            cls._stream_handler.setLevel(logging.INFO)
            cls._stream_handler.setFormatter(ColoredFormatter(cls.LOG_FORMAT_FOR_CMD))
            cls._logger.addHandler(cls._stream_handler)

            logs_dir = os.path.join(output_dir, 'logs')
            os.makedirs(logs_dir, exist_ok=True)

            file_path = os.path.join(logs_dir, f'{datetime.now().strftime("%Y_%m_%d-%H_%M")}.log')
            cls._file_handler = logging.FileHandler(file_path, 'w', 'utf-8')
            cls._file_handler.setLevel(logging.INFO)
            cls._file_handler.setFormatter(logging.Formatter(cls.LOG_FORMAT_FOR_FILE))
            cls._logger.addHandler(cls._file_handler)
        return cls._logger

    @classmethod
    def info(cls, message: str):
        cls._get_logger().info(message)

    @classmethod
    def debug(cls, message: str):
        cls._get_logger().debug(message)

    @classmethod
    def warn(cls, message: str):
        cls._get_logger().warning(message)

    @classmethod
    def fatal(cls, message: str, exception_type=Exception) -> NoReturn:
        cls._get_logger().error(message)
        raise exception_type(message)