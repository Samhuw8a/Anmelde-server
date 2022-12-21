from re import error


class Error(Exception):
    def __init__(self,message:str) -> None:
        self.msg=message
        super().__init__(message)

    def __str__(self) -> str:
        return self.msg

class Error_handler():
    def __init__(self,*er) -> None:
        errs:list = []
        for e in er:
            errs.append(e)
        self.errors:tuple = tuple(errs)

    def __str__(self)->str:
        msg = ""
        msg+=f"{len(self.errors)} Exception found!\n"
        msg+="-"*30+"\n"
        for e in self.errors:
            msg+=str(e)+"\n"
        return msg

    def raise_exc(self)->None:
        raise Exception(*self.errors)
