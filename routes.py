from flask import Flask, request, render_template
import database
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

    return
@app.route('/login', methods = ["PUT"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    return
@app.route('/creategame', methods = ["POST"])
def createGame():
    uniquestring = request.form["unqstr"]
    maxPlayers = request.form["mxpl"]
    return
@app.route('/startgame', methods = ["PUT"])
def startGame():
    uniqueString = request.form["unqstr"]
    gameID = request.form["gid"]
    return
@app.route('/joingame', methods = ["PUT"])
def joinGame():
    uniqueString = request.form["unqstr"]
    gameID = request.form["gid"]
    return
@app.route('/unlockedtags', methods = ["GET"])
def viewUnlockedTags():
    uniqueString = request.form["unqstr"]
    return
@app.route('/edittag', methods = ["PUT"])
def editActiveTag():
    uniqueString = request.form["unqstr"]
    tagID = request.form["tid"]
    return
@app.route('/getchat', methods = ["GET"])
def getChat():
    uniqueString = request.form["unqstr"]
    return
@app.route('/checkgeneration', methods = ["GET"])
def checkForNewGeneration():
    uniqueString = request.form["unqstr"]
    return
@app.route('/definegeneration', methods = ["PUT"])
def defineANewGeneration():
    uniqueString = request.form["unqstr"]
    characterstics = request.form["chr"]#this is going to be a string and will need to be processed.
    return
@app.route('/message', methods = ["PUT"])
def sendMessage():
    uniqueString = request.form["unqstr"]
    message = request.form["msg"]
    return