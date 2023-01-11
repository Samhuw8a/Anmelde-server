from typing import Any

class Arg:
    def __init__(self, description:str) -> None:
        self.desc = description

    def help(self) -> str:
        return self.desc
    
class Option(Arg):
    def __init__(self, description: str, *options: Any) -> None:
        super().__init__(description)
        self.options = options


def main()->None:
    o = Option("Test", "adsf", 2)

if __name__ == "__main__":
    main()
