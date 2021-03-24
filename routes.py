from flask import Flask, request, render_template
import database
import threading
import time
import serverManager
from app import app

"""
request.form.get('
@app.route('/something', methods = ["GET"])
def somethingfunction():
    return data
request.form.get(
"""

@app.route('/signup', methods = ["POST"])
def signUp():
    username = request.form["username"]
    password = request.form["password"]
    database.addNewUser(username, password)
    return
@app.route('/login', methods = ["PUT"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    global server
    server.lock.acquire()
    if database.verifyPassword(username, password):
        value = server.logIn(username + database.getActiveCosmetic(username))
        server.lock.release()
        return value
    server.lock.release()
    return
@app.route('/creategame', methods = ["POST"])
def createGame():
    uniquestring = request.form["unqstr"]
    maxPlayers = request.form["mxpl"]
    global server
    server.lock.acquire()
    value =  server.newGame(uniquestring, maxPlayers)
    server.lock.release()
    return value

@app.route('/startgame', methods = ["PUT"])
def startGame():
    uniqueString = request.form["unqstr"]
    gameID = request.form["gid"]
    global server
    server.lock.acquire()
    server.startGame(uniqueString, gameID)
    server.lock.release()
    return

@app.route('/joingame', methods = ["PUT"])
def joinGame():
    uniqueString = request.form["unqstr"]
    gameID = request.form["gid"]
    global server
    server.lock.acquire()
    server.joinGame(uniqueString, gameID)
    server.lock.release()
    return

@app.route('/unlockedtags', methods = ["GET"])
def viewUnlockedTags():
    uniqueString = request.args.get("unqstr")
    global server
    server.lock.acquire()
    value = database.getUnlockedCosmetics(server.getUsername(uniqueString))
    server.lock.release()
    return value

@app.route('/edittag', methods = ["PUT"])
def editActiveTag():
    uniqueString = request.form["unqstr"]
    tagID = request.form["tid"]
    global server
    server.lock.acquire()
    username = server.getUsername(uniqueString)
    database.changeActiveCosmetic(username, tagID)
    server.updateName(username+database.getActiveCosmetic(username),uniqueString)
    server.lock.release()

@app.route('/getchat', methods = ["GET"])
def getChat():
    uniqueString = request.args.get("unqstr")
    global server
    server.lock.acquire()
    value = server.getChat(uniqueString)
    server.lock.release()
    return value

@app.route('/checkgeneration', methods = ["GET"])
def checkForNewGeneration():
    uniqueString = request.args.get("unqstr")
    global server
    server.lock.acquire()
    value = server.checkForNewGeneration(uniqueString)
    server.lock.release()
    return value

@app.route('/definegeneration', methods = ["PUT"])
def defineANewGeneration():
    uniqueString = request.form["unqstr"]
    characteristics = request.form["chr"]#this is going to be a string and is processed.
    size = request.form["size"]
    global server
    server.lock.acquire()
    value = server.newGeneration(characteristics.split(), size, uniqueString)
    server.lock.release()
    return value

@app.route('/message', methods = ["PUT"])
def sendMessage():
    uniqueString = request.form["unqstr"]
    message = request.form["msg"]
    global server
    server.lock.acquire()
    server.sendMessage(message, uniqueString)
    server.lock.release()

@app.route('/checkname', methods = ["GET"])
def checkName():
    print("hey")
    name = request.args.get("name")
    return str(database.checkIfNameIsTaken(name))


server = serverManager.ServerManager()
def asyncticker(timePerTick):
    prevtime = time.time()
    global server
    while True:
        print(".")
        newTime = time.time()
        timeBetweenTicks = newTime - prevtime
        prevtime = newTime
        server.lock.acquire()
        server.tick(timePerTick)
        server.lock.release()
        time.sleep(timePerTick - timeBetweenTicks)
def ticker(timePerTick):
    prevtime = time.time()
    print("hey1")
    global server
    global running
    if running:
        return
    else:
        running = True
    print("hey2")
    server.lock.acquire()
    server.tick(timePerTick)
    print("hey3")
    server.lock.release()
    newTime = time.time()
    timeBetweenTicks = newTime - prevtime
    time.sleep(max(0,timePerTick - timeBetweenTicks))
    running = False
    print(running)
    print("---")

running = False
if __name__ == "__main__":
    t1 = threading.Thread(target=app.run, kwargs={"threading":True})
    t1.start()
t2 = threading.Thread(target = server.tick, args = (1,))
t2.start()