class Error(Exception):
    pass


class ConfigError(Error):
    pass


class SQLError(Error):
    pass


class UserError(Error):
    pass


class TokenError(Error):
    pass


class ToManyTriesError(TokenError):
    pass


class TokenTimeOutError(TokenError):
    pass


def main() -> None:
    raise UserError("User")
    raise SQLError("SQL")
    raise ConfigError("Config")
    raise Error("Error")


if __name__ == "__main__":
    main()
