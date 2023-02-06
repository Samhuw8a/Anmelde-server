class Error(Exception):
    def __init__(self, message: str) -> None:
        self.msg = message
        super().__init__(message)

    def __str__(self) -> str:
        return self.msg


class ConfigError(Error):
    pass


class SQLError(Error):
    pass


class UserError(Error):
    pass


def main() -> None:
    raise UserError("User")
    raise SQLError("SQL")
    raise ConfigError("Config")
    raise Error("Error")


if __name__ == "__main__":
    main()
