from main import Event_handler
from errors import Error, UserError, SQLError, ConfigError
import time

def beenden()->None:
    print("aborting Process!")
    print("Guet Nacht")
    exit()

def main()->None:
    abort = False
    handler = Event_handler()
    while True:
        try: handler.main()
        except UserError as e:
            print(e)
        except KeyboardInterrupt:
            abort = True

        if abort: beenden()

        try:time.sleep(5)
        except KeyboardInterrupt:
            beenden()
if __name__ == "__main__":
    main()
