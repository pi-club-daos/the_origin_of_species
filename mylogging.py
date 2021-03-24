import datetime
def log(func):
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as e:
            with open("logging.txt", "a+") as myfile:
                myfile.write(f"{datetime.datetime.now()}: error {e}, in function {func.__name__}.\n")
    return wrapper