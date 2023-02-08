import logging
import functools
import sys
import os
from datetime import datetime
import traceback
from settings_cls import Log_conf
from typing import Callable, Any, Type


def log_error(ex: Any, logger: logging.Logger, error_dir: str) -> None:
    dt = datetime.now()
    nw = dt.strftime("%d:%m_%H:%M")
    file = error_dir + f"{nw}.log"
    logger.error(f"An Error ({type(ex)}) occurred while executing (see: {file})")
    path = os.path.dirname(__file__) + file
    with open(path, "a") as log:
        traceback.print_exc(file=log)


def init_logger(l_conf: Log_conf) -> logging.Logger:
    path = os.path.dirname(__file__) + l_conf.log_file
    logger = logging.Logger("main")

    file_formater = logging.Formatter(l_conf.file_logging_format)
    stream_formater = logging.Formatter(l_conf.stream_logging_format)

    if l_conf.output:
        streamhandler = logging.StreamHandler(sys.stdout)
        streamhandler.setLevel(l_conf.stream_level)
        streamhandler.setFormatter(stream_formater)
        logger.addHandler(streamhandler)

    filehandler = logging.FileHandler(path)
    filehandler.setFormatter(file_formater)
    filehandler.setLevel(l_conf.file_level)
    logger.addHandler(filehandler)

    return logger


def with_logging(logger: logging.Logger) -> Callable:
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            logger.debug(f"Calling {func.__name__}")
            value = func(*args, **kwargs)
            logger.debug(f"Finished executing {func.__name__}")
            return value

        return wrapper

    return decorator
