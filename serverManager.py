import game
import string
class ServerManager:

    def __init__(self):
        self.games = {}#a dictionary with the key as the id of each games and the value as a tuple of the game instance and the time it was started at and the name of the creator
        self.players = {}# a dictionary with the key as the string sent to the user when they log in and the value as a tuple of the player name and the time they logged in and the id of the game they are in
        self.newGenerations = {}# a dictionary with the key as the player name and the value as a tuple with the number of generations they need to choose characteristics for and the number of points they have and the existing characteristics

    def logIn(self, username):
        #the password will have already been checked in the flask file with the database
        #the username will contain the players username as well as any titles they have unlocked
        toDelete = []
        for id in self.players:
            if self.players[id][0] == username:
                toDelete.append(id)
        for i in toDelete:
            del(self.players[i])
        uniqueString = self.generateUniqueString(50)
        self.players[uniqueString] = (username, time.time(), None)
        return uniqueString

    def generateUniqueString(self, length):
        #method from here https://www.educative.io/edpresso/how-to-generate-a-random-string-in-python
        letters = string.ascii_letters
        return ''.join(random.choice(letters) for i in range(length))

    def newGame(self, creator):
        id = self.generateUniqueString(5)
        self.games[id] = (game.Game(500, self), time.time(), creator)
        return id

    def joinGame(self, playerID, gameID):
        self.games[gameID][0].addSpecies(self.players[playerID][0])
        self.players[playerID][2] = self.games[gameID]

    def startGame(self, playerID, gameID):
        #this starts the game the player is in if the player is the creator
        if self.games[gameID][2] == self.players[playerID][0]:
            self.games[gameID][0].started = True
            return True
        return False

    def getChat(self, playerID):
        if self.players[playerID][2]:
            return self.players[playerID][2].getChat()
        else:
            return "you aren't currently in a game im confused why you would ask this"

    def tick(self, timeBetweenTicks):
        #this function should be called in a seperate thread and will constantly tick the server
        while True:
            timer = time.time()
            #if security is a concern(which it currently isn't) you would check that all of the players haven't been logged in for too long
            for gameID in self.games:
                if self.games[gameID][1] - time.time() > 10800:#this means that if a game is older than 3 hours it will be deleted. this may need to be extended and is a magic number
                    del(self.games[gameID])
                else:
                    self.games[gameID][0].tick()
            if time.time() - timer < timeBetweenTicks:
                time.sleep(timeBetweenTicks - (time.time() - timer))
            else:
                #if this is ever reached then that means that the tick speed specified is too fast as the server cannot keep up.
                print("error: server running slower than designated tick speed")

    def checkForNewGeneration(self, ID):
        #this function should be called by the client when getChat is called and will tell them if they need to define a new generation, and how
        return

    def newGeneration(self, characteristics, size):
        #this function should be called by the client when the player has defined a new generation
        return

    def sendMessage(self, message):
        #this function contains the processes for the message to be sent to all the players.
        return

    def playerIsDead(self, place, playerID):
        #this function contains the processes for when a player dies, and does the necessary processes so that the player is given any rewards they deserve. it should be called by the client as there is no incentive to fake this.
        if self.players[playerID][2] == None:#this means the player wasn't in a game so couldn't have died
            return
        if len(self.players[playerID][2][players]) > place:#this means that they can't have come in this position as there are more than this number of people remaining
            return
        #do stuff here this function is not finished
        return
