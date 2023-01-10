import logging
from errors import Error, SQLConnectionError, UserError, ConfigError

class Logger():
    def __init__(self)->None:
        raise NotImplementedError

    def log_error(self)->None:
        raise NotImplementedError

    def log_user_auth(self)->None:
        raise NotImplementedError

