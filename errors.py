class Error(Exception):
    def __init__(self,message:str) -> None:
        self.msg=message
        super().__init__(message)

    def __str__(self) -> str:
        return self.msg
