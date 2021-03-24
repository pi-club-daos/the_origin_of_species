import mylogging

@mylogging.log
def hello():
    print("hi")

@mylogging.log
def hellobroken():
    print("hi" + 3)

hello()
hellobroken()