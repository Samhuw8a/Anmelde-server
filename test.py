import errors
import handling
import email_handler

def main()->None:
    # Errors
    e = errors.Error("test")
    h = errors.Error_handler(e,StopAsyncIteration)
    assert str(e)=="test"
    assert str(h)

if __name__ == "__main__":
    main()
