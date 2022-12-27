from main import Event_handler
import time

def main()->None:
    handler = Event_handler()
    while True:
        handler.main()
        time.sleep(5)
if __name__ == "__main__":
    main()
