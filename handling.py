class User():
    def __init__(self,mail:str,username:str,name:str) -> None:
        self.mail:str     = mail 
        self.username:str = username
        self.name:str     = name
    def __repr__(self) -> str:
        return f"User({self.mail},{self.username},{self.name})"

class Parser():
    pass

class Handler():
    pass
