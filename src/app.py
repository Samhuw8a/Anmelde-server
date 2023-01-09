from main import Event_handler
from errors import Error
import time

def main()->None:
    handler = Event_handler()
    while True:
        try: handler.main()
        except Error as e:
            print(e)
        time.sleep(5)
if __name__ == "__main__":
    main()
