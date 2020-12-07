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
    if database.verifyPassword(username, password):
        return server.logIn(username + database.getActiveCosmetic(username))
    return
@app.route('/creategame', methods = ["POST"])
def createGame():
    uniquestring = request.form["unqstr"]
    maxPlayers = request.form["mxpl"]
    global server
    return server.newGame(uniquestring, maxPlayers)

@app.route('/startgame', methods = ["PUT"])
def startGame():
    uniqueString = request.form["unqstr"]
    gameID = request.form["gid"]
    global server
    server.startGame(uniqueString, gameID)
    return

@app.route('/joingame', methods = ["PUT"])
def joinGame():
    uniqueString = request.form["unqstr"]
    gameID = request.form["gid"]
    global server
    server.joinGame(uniqueString, gameID)
    return

@app.route('/unlockedtags', methods = ["GET"])
def viewUnlockedTags():
    uniqueString = request.form["unqstr"]
    global server
    return database.getUnlockedCosmetics(server.getUsername(uniqueString))

@app.route('/edittag', methods = ["PUT"])
def editActiveTag():
    uniqueString = request.form["unqstr"]
    tagID = request.form["tid"]
    global server
    username = server.getUsername(uniqueString)
    database.changeActiveCosmetic(username, tagID)
    server.updateName(username+database.getActiveCosmetic(username),uniqueString)

@app.route('/getchat', methods = ["GET"])
def getChat():
    uniqueString = request.form["unqstr"]
    global server
    return server.getChat(uniqueString)

@app.route('/checkgeneration', methods = ["GET"])
def checkForNewGeneration():
    uniqueString = request.form["unqstr"]
    global server
    return server.checkForNewGeneration(uniqueString)

@app.route('/definegeneration', methods = ["PUT"])
def defineANewGeneration():
    uniqueString = request.form["unqstr"]
    characteristics = request.form["chr"]#this is going to be a string and will need to be processed.
    size = request.form["size"]
    global server
    return server.newGeneration(characteristics.split(), size, uniqueString)

@app.route('/message', methods = ["PUT"])
def sendMessage():
    uniqueString = request.form["unqstr"]
    message = request.form["msg"]
    global server
    server.sendMessage(message, uniqueString)

server = serverManager.ServerManager()

def ticker(timePerTick):
    prevtime = time.time()
    global server
    while True:
        newTime = time.time()
        timeBetweenTicks = newTime - prevtime
        prevtime = newTime
        server.tick(timeBetweenTicks)
        time.sleep(timePerTick - timeBetweenTicks)
