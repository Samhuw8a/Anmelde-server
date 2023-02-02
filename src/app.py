from os import pardir
from main import OUTPUT, Event_handler
from errors import Error, UserError, SQLError, ConfigError
import sys
import logging
import argparse
import time

OUTPUT = bool()
LOG_FILE="/../logs/log.log"
STREAM_LOGGING_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
FILE_LOGGING_FORMAT   = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
FILE_LEVEL  = logging.INFO
STREAM_LEVEL= logging.DEBUG

def beenden()->None:
    print("aborting Process!")
    print("Guet Nacht")
    exit()

def init_argparser()->argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="Anmelde-Server",
        description= "Das Anmelde-Programm des KSRMinecraft-server"
                                    )
    parser.add_argument("-l","--log_file",default=LOG_FILE)
    parser.add_argument("-v","--verbose",action="store_true")
    return parser 

def main()->None:
    global OUTPUT
    abort = False
    parser= init_argparser()
    args = parser.parse_args(sys.argv[1:])
    OUTPUT = args.verbose
    log_file = args.log_file
    stream_logging_format = STREAM_LOGGING_FORMAT
    file_logging_format = FILE_LOGGING_FORMAT
    file_level=FILE_LEVEL
    stream_level=STREAM_LEVEL
    handler = Event_handler(log_file,stream_logging_format,file_logging_format,file_level,stream_level)
    #  while True:
    #      try: handler.main()
    #      except UserError as e:
    #          print(e)
    #      except KeyboardInterrupt:
    #          abort = True
    #
    #      if abort: beenden()
    #
    #      try:time.sleep(5)
    #      except KeyboardInterrupt:
    #          beenden()
if __name__ == "__main__":
    main()
