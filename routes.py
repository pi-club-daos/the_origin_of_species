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
    username = request.form[""]
    return
@app.route('/login', methods = ["GET"])
def login():
    return
@app.route('/creategame', methods = ["GET"])
def createGame():
    return
@app.route('/startgame', methods = ["GET"])
def startGame():
    return
@app.route('/joingame', methods = ["GET"])
def joinGame():
    return
@app.route('/unlockedtags', methods = ["GET"])
def viewUnlockedTags():
    return
@app.route('/edittag', methods = ["GET"])
def editActiveTag():
    return
@app.route('/getchat', methods = ["GET"])
def getChat():
    return
@app.route('/checkgeneration', methods = ["GET"])
def checkForNewGeneration():
    return
@app.route('/definegeneration', methods = ["GET"])
def defineANewGeneration():
    return
@app.route('/message', methods = ["GET"])
def sendMessage():
    return