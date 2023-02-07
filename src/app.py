from os import pardir
from main import Event_handler
from errors import Error, UserError, SQLError, ConfigError
from _logging import init_logger, log_error
from settings_cls import Log_conf
import sys
import logging
import argparse
import time

OUTPUT = True
LOG_FILE = "/../logs/log.log"
ERROR_DIR = "/../logs/errors/"
STREAM_LOGGING_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
FILE_LOGGING_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
FILE_LEVEL = logging.INFO
STREAM_LEVEL = logging.DEBUG


def beenden() -> None:
    print("aborting Process!")
    print("Guet Nacht")
    exit()


def init_argparser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="Anmelde-Server",
        description="Das Anmelde-Programm des KSRMinecraft-server",
    )
    parser.add_argument("-l", "--log_file", default=LOG_FILE)
    parser.add_argument("-v", "--verbose", action="store_true")
    parser.add_argument("-t", "--timeout", action="store", default=7, type=int)
    return parser


def main() -> None:
    abort = False

    parser = init_argparser()
    args = parser.parse_args(sys.argv[1:])

    output = args.verbose
    log_file = args.log_file
    stream_logging_format = STREAM_LOGGING_FORMAT
    file_logging_format = FILE_LOGGING_FORMAT
    file_level = FILE_LEVEL
    stream_level = STREAM_LEVEL
    timeout = args.timeout

    log_config = Log_conf(
        log_file=log_file,
        stream_logging_format=stream_logging_format,
        file_logging_format=file_logging_format,
        file_level=file_level,
        stream_level=stream_level,
        output=output,
    )
    logger = init_logger(log_config)
    handler = Event_handler(logger)
    while not abort:
        try:
            handler.main()
        except UserError as e:
            print(e)

        except KeyboardInterrupt:
            abort = True

        except Exception as e:
            log_error(e, logger, ERROR_DIR)
            beenden()

        if abort:
            beenden()

        try:
            time.sleep(timeout)
        except KeyboardInterrupt:
            beenden()


if __name__ == "__main__":
    main()
