import time
import random
import noise
import pathfinding
import nameGeneration
import mergeSort
class Game:
    def __init__(self, mapsize, server, maxPlayers):
        self.started = False
        self.mapsize = mapsize
        self.server = server#the instance of the server for networking
        self.startTime = time.time()
        self.players = {}#a dict of all the players(instances of the species class) in the game
        self.items = []#a list of all the instances of the item class to iterate through when
        self.map = self.generateMap(mapsize)#the map the game takes place in. A grid of a fixed size with random spaces that are not traversable. a 2d array of 1s and 0s
        self.chat = []#the global chat for the game with the time
        self.time = 0#the number of ticks since the beginning of the game
        self.creatureSize = 1#this is a magic number
        self.alivePlayers = 0
        self.maxPlayers = maxPlayers
        self.full = self.alivePlayers == self.maxPlayers

    def getPlayersByPoints(self):
        return mergeSort.mergeSort(self.players).keys()

    def getMapSize(self):
        return self.mapsize

    def addItem(self,item):
        self.items.append(item)
    def item(self, index):
        return self.items[index]

    def numItems(self):
        return len(self.items)

    def getChat(self, ID):
        return self.players[ID].getChat()

    def generateMap(self, mapsize):
        #generate the map using simplex noise so it looks somewhat realistic if presented in a graphical interface. this should also mean that there are no open spaces that are shut off
        octaves = 1
        freq = 0.15 * mapsize#this means the map will not change based on mapsize
        seed = random.randint(-1000000, 1000000)#if you put a random number generator in a generator it generates a different number each time and becomes random noise so it must be here instead
        map = [[1  if noise.snoise2(x/freq, y/freq, octaves, base=(seed)) > 0.5 else 0 for y in range(mapsize)] for x in range(mapsize)]#for whatever reason the base parameter of this function must be less than 1 million
        return map


    def newGeneration(self, ID, characteristics, size):
        self.players[ID].newGeneration(characteristics, size)
        self.updateChat("system: there is a new generation of %s" % (ID))

    def addSpecies(self, ID):
        #a function to add new players.
        if ID in self.players.keys():
            return
        self.alivePlayers += 1
        self.updateChat("system: %s has joined the game" % (ID))
        self.players[ID] = Species(ID, self.creatureSize, self)
        self.items += self.players[ID].firstGeneration()


    def speciesIsDead(self, species):
        #does the appropriate processes when a species dies, including updating the players profile
        self.alivePlayers -= 1
        self.updateChat("system: %s is extinct" % (species.ID))
        if self.alivePlayers == 2:#this means someone has won the game
            self.updateChat("The game is over")
            for i in self.players.keys():
                if self.players[i].__class__.__name__ == "Species":
                    self.speciesIsDead(self.players[i])
                    break

        #talk to the server about how they did in the game
        del(self.players[species.ID])
        species.updateChat("system: you came in %s place" % ((lambda n: "%d%s" % (n,"tsnrhtdd"[(n/10%10!=1)*(n%10<4)*n%10::4]))(self.alivePlayers + 1)))#ordinal number converter sourced from here: https://stackoverflow.com/questions/9647202/ordinal-numbers-replacement

        self.players[species] = Ghost(species.getChat(), self)#replaces the player with a ghost that can still see the chat and send messages
        del(species)


    def tick(self):
        #this increases the time and tells every item to make decisions, then tells every item to act on the decisions
        if not self.started:#this means time does not pass until the game has started
            return
        self.time += 1
        for item in self.items:
            item.makeDecisions()
        for item in self.items:
            item.move()


    def pathFind(self, loc1, loc2):
        #this function finds a path between two points and returns the path as a list of tuples
        return pathfinding.astar(self.map, loc1, loc2)


    def plantIsEaten(self, plant):
        #this function removes the plant and adds a new one in a random empty space. An item can be in the space the plant is spawned, but it must not be a hole
        for item in self.items:
            if item == plant:
                del(item)
                del(plant)
                break
        foundEmptySpace=False
        space = (random.randint(0, self.mapsize), random.randint(0, self.mapsize))
        if self.map[space[0]][space[1]] == 0:
            foundEmptySpace = True
        #this just checks the map it doesn't check for other items because multiple items can occupy one space
        while not foundEmptySpace:
            space = (random.randint(0,self.mapsize), random.randint(0,self.mapsize))
            if self.map[space[0]][space[1]] == 0:
                foundEmptySpace = True
        self.addItem(Plant(self, space, random.randint(1,5), True if random.randint(0,10)==0 else False))#the numbers in the random generators are magic numbers and should be replaced with parameters/class variables

    def updateChat(self, message):
        #updates the chat and updates the chat of every species in the format(time, message
        msg = (time.time(), message)
        self.chat.append(msg)
        for player in self.players:
            player.updateChat(msg)

#the base class for all the different items/creatures that can exist in the game
class Item:
    def __init__(self, game, location, size):
        self.location = location#this is the location of the item on the map
        self.game = game#this is the instance of the game class that the item belongs to. it allows the item to tell the game class to do certain things i.e. if a creature has offspring, a plant is eaten
        self.size = size#this is the size of the item, important for eating

    def compareLocation(self, otherLocation):
        return self.location == otherLocation

    def getSize(self):
        return self.size

    def getLocation(self):
        return self.location

    def isInSight(self, playerLoc):
        #this function checks if the item is visible by the player in playerLoc.
        loc = (playerLoc[0] - self.location[0], playerLoc[1] - self.location[1])
        return loc[0]**2 + loc[1]**2


    def interestingCharacteristics(self):
        #this function returns the characteristics that affect the decisions that another item might take
        raise Exception("function not implemented")

    def eaten(self, other):
        # this function does the neccessary processes for if the creature is eaten. It will only be called by the creature that ate it
        raise Exception("function not implemented")

    def move(self):
        #this function exists so we can call this function on  any item and not get an error
        pass

    def makeDecisions(self):
        #this function exists so we can call this function on  any item and not get an error
        pass



class Creature(Item):
    def __init__(self, game, location, size, name, species, characteristics, generation, minPointsEnergy, maxEnergy, ID):
        self.ID = (ID, name)#this is used for the family tree and is seperate to the species ID which is the player name. This includes the creature name to make the family tree more readable
        Item.__init__(self, game, location, size)
        self.name = name#a randomly generated name for the creature
        self.age = 0#the age of the item. This doesn't matter for plants. Age is the number of ticks since the item was created.
        self.species = species#the player who owns this creature
        self.characteristics = characteristics#the characteristics of the creature stored in a dictionary with their state i.e. for size this would be the size as a number
        self.energy = maxEnergy#the current energy of the creature. If this reaches zero the creature will die. It decreases with time and movement and increases by eating
        self.offspring = []#this is a list of the IDs of the offspring of this creature. This enables the family tree to be created. Not implemented yet(probably never so remove if not implemented)
        self.generation = generation#the generation that this creature belongs to. Used by the creature class to decide if the player needs to decide new characteristics
        self.minPointsEnergy = minPointsEnergy#the amount of energy required to gain a point when move is called
        self.maxEnergy = maxEnergy#the the maximum energy the creature can have
        self.nextLoc = location#the location that the creature will move to when move is called
        self.dist = 0

    def getID(self):
        return self.ID

    def getName(self):
        return self.name

    def getSpecies(self):
        return self.species

    def characteristic(self, key):
        return self.characteristics[key]



    def calculateMove(self, destination):
        #this function calculates the move for the creature. It will use pathfinding, and return the space that the player should move to based on the speed of the creature
        path = self.game.pathFind(self.location, destination)
        self.dist = min(len(path), self.characteristics["speed"])
        self.nextLoc = path[self.dist]#this will get the speed from the characteristics and move to that space in the path. This means speed is equal to the number of steps moved in one tick

    def move(self):
        #this function moves the creature based on the move from calculateMove. all creatures should be moved at the same time after decisions have all been made. The creatures energy should decrease more if it moves but should always be decreased here. The species points should increase if it has energy over minpointsenergy
        self.energy -= self.dist * self.characteristics["energy per distance moved"] * self.size
        self.location = self.nextLoc

    def haveOffspring(self):
        #this function does the neccessary processes for if the creature wants to have offspring, including prompting the player to make decisions if it is the first offspring of its generation
        self.offspring.append(self.species.addOffspring(self.generation+1))
        self.species.updateChat("system: %s has had offspring" % (self.name))


    def eat(self, item):
        # this function does the necessary processes for if the creature eats something. the amount of energy added should be decided by the size of the item
        if item.__class__.__name__ == "Plant":
            self.species.updateChat("system: %s ate a plant" % (self.name))
            if(not self.characteristics["can eat poisonous plants"]):#sees if it is eating a plant and the creature can be killed by poisonous plants
                if item.poisonous:
                    self.species.updateChat("system: the plant %s ate was poisnous and it died" % (self.name))
                    item.eaten()
                    self.dead()
                    return

        else:
            self.species.updateChat("system: %s ate %s of species %s" % (self.name, item.name, item.species.ID))
        self.energy += self.characteristics["energy per unit size"] * item.getSize()
        item.eaten()
        if self.energy > self.maxEnergy:
            self.energy = self.maxEnergy



    def getInformation(self):
        #this function queries the isInSight of every item and returns a list of all that return true, along with the distance
        itemsInSight = []
        distSquared = self.characteristics["maximum view dist squared"]
        for index in range(self.game.numItems()):
            itemDist = self.game.item(index).isInSight(self.location)
            if itemDist > distSquared:
                continue
            if self.game.item(index).__class__.__name__ == self.__class__.__name__:
                if random.random() < self.game.item(index).characteristics["camoflague"]:
                    itemsInSight.append((itemDist, self.game.item(index)))
        #sort itemsInSight here using a merge sort and remove the distances
        return itemsInSight

    def makeDecisions(self):
        #this function makes decisions based on its characteristics and the interesting and based on the closest items first. As soon as one decision is made it will be done with this function.
        self.age += 1
        #see if is still a child
        if self.age < self.characteristics["time to grow up"]:
            self.species.updateChat("system: %s grew up" % (self.name))
            return
        #see if lifespan is up
        if self.age > self.characteristics["lifespan"]:
            self.species.updateChat("system: %s died of old age" % (self.name))
            self.dead()
            return
        itemsInSight = self.getInformation()
        if len(itemsInSight) == 0:
            #moves towards a random place
            self.calculateMove((random.randint(0,self.game.getMapSize()), random.randint(0,self.game.getMapSize())))
            return
        for item in itemsInSight:
            #see if can mate and mate if so
            if item.__class__.__name__ == self.__class__.__name__:#if it is also a creature
                if item.species == self.species:
                    if not item.compareLocation(self.location):
                        self.calculateMove(item.getLocation())
                        return
                    elif random.randint(0,self.characteristics["chance to have offspring"]) == 0:
                        self.haveOffspring()
                        return
                elif item.canEat(self) and self.characteristics["can recognise predators"]:#if it can eat you
                    #run away. While it would make sense to run in the opposite direction this will involve multiple calculations which may take a long time to calculate so for now it will just run in a random direction. This could be described as emulation of panic. Running in the opposite direction should be tested when the game is complete to see if there is a notable performance hit, however.
                    self.calculateMove((random.randint(0, self.game.getMapSize()), random.randint(0, self.game.getMapSize())))
                    return
                # see if can eat and eat if so. if animal must be carniverous and less than size can eat. if plant must be not poisonous if they have can see poison and not eat it
                if self.characteristics["carnivorous"]:#if it can eat creatures
                    if self.canEat(item):#if it can eat this creature
                        if not item.compareLocation(self.location):#move towards it if they aren't in the same location
                            self.calculateMove(item.getLocation())
                            return
                        else:
                            self.eat(item)
                            return
            else:
                #if it is not a creature it must be a plant
                if self.characteristics["can eat poison"]:#if it can eat poisonous plants it should always eat the plant
                    if not item.compareLocation(self.location):
                        self.calculateMove(item.getLocation())
                        return
                    else:
                        self.eat(item)
                        return
                else:
                    if not(self.characteristics["can see poison"] or item.poionous):#if it can't see poison or the plant isn't poisonous eat the plant
                        if not item.compareLocation(self.location):
                            self.calculateMove(item.getLocation)
                            return
                        else:
                            self.eat(item)
                            return

    def eaten(self, other):
        # this function does the neccessary processes for if the creature is eaten. It will only be called by the creature that ate it
        self.species.updateChat("system: %s was eaten by %s of species %s" % (self.name, other.name, other.species.ID))
        self.dead()

    def dead(self):
        #this function does the necessary processes for if the creature dies
        self.species.creatureIsKilled(self)

    def canEat(self, other):
        #this function does the necessary processes to check if this creature can eat the creature other.
        if other.species == self.species or not self.characteristics["carnivorous"]:
            return False
        return other.getSize < self.characteristics["size can eat"] * self.size



class Plant(Item):
    #change so poisonous is in a getter
    def __init__(self, game, location, size, poisonous):
        Item.__init__(self, game, location, size)
        self.poisonous = poisonous

    def eaten(self, other):
        # this function does the neccessary processes for if the creature is eaten. It will only be called by the creature that ate it
        self.game.plantIsEaten(self)
class Player:
    #parent class for the classes controlled by the player (for now these are only ghost and species)
    def __init__(self, chat, game):
        self.chat = chat
        self.game = game
        self.chatLastRead = time.time()


    def getChat(self):
        #a function to get the unread chat and delete the read chat. This could be made more effecient by deleting the whole chat when it is read, however this is likely to potentially cause issues if there a functions running in different threads
        chat = ""#the chat to return, does not include the timestamps
        for message in self.chat:
            if message[0] < self.chatLastRead:
                del(message)
            else:
                chat += "\n" + (message[1])
        self.chatLastRead = time.time()
        return chat

    def updateChat(self, message):
        #updates the chat in the format (time, message)
        msg = (time.time(), message)
        self.chat.append(msg)

    def sendMessage(self, message):
        #sends a message to the global game chat, and therefore all players
        message = self.ID + ": " + message
        self.game.updateChat(message)
    def getPoints(self):
        return 0

class Species(Player):

    def __init__(self, ID, initialSize, game):
        Player.__init__(self, [], game)
        self.creatureID = 0
        self.creatures = []#a list of all the living creatures in the species
        self.familytree = {}#a graph of all the dead creatures' IDs and
        self.ID = ID#the ID of this species that the player who is controlling this species needs to make actions
        self.characteristics = [{"speed" : 1,#the distance that the creature can move per step i time
                                "maximum view dist squared" : 1,#the maximum distance that the creature can see, squared
                                 "size can eat" : 0,#the biggest size of creature that this creature can eat, as a ratio
                                 "carnivorous":False,#if the creature can eat other creatures
                                 "number of offspring" : 1,#the number of offspring that will be had by the creature when it has offspring
                                 "time to grow up" : 100,#this is a magic number. also the number of steps in time it will take for the creature to be able to move
                                 "energy per unit size" : 100,#this is a magic number. also the amount of energy that a different creature will gain when eating this creature. this should probably be fixed and not here.
                                 "energy per distance moved" : 100,#this is a magic number. also the amount of energy that will be used by the creature when it is moving
                                 "lifespan" : 0,#the number of steps in time after which the creature will die of old age
                                 "camouflage" : 0,#the chance that another creature won't see this animal. this includes mates
                                 "can recognise predators": False,#if the creature can see predators, and therefore run away
                                 "can eat poison" : False,#if the creature can eat poisonous plants
                                 "can see poison" : False,#if the creature can see poisonous plants so it knows not to eat them
                                 "chance to have offspring" : 10#1/ the probability that an offspring will be had at a given opportunity
                                }]#a list of the characteristics of each generation
        self.points = 100#the points of the species, used to purchase new characteristics. Characteristics cost more the more creatures there are. edit this number to change the number of points players start with
        self.size = [initialSize]#the size of members of the species as a list split by generations
        self.needNewGeneration = True#change to be read with a getter
    def getPoints(self):
        return self.points

    def addOffspring(self, generation, parent):
        #adds a new offspring
        if(len(self.characteristics) < generation):
            #tell the server to ask the player to specify the characteristics for the next genreation. it will ignore this if it has already asked
            self.needNewGeneration = True
            return#this means that the player hasn't specified the characteristics for this generation yet so this child can't be had.
        elif(len(self.characteristics) == generation):#this means that this creature will belong to the youngest generation
            #tell the server to ask the player to specify the characteristics for the next generation
            self.needNewGeneration = True
        else:
            self.needNewGeneration = False
        newCreature = Creature(self.game, parent.getLocation(), self.size[generation-1], self.generateRandomName(), self, self.characteristics[generation-1], generation, 50, 100, self.creatureID)#these are magic numbers and should be replaced
        self.creatures.append(newCreature)
        self.game.addItem(newCreature)
        self.creatureID += 1


    def generateRandomName(self):
        #choose a random name
        return nameGeneration.generateName()

    def firstGeneration(self):
        #a function that creates the first generation of creatures and returns a list of them. The location must be a space on the map with a value of zero
        characteristics =  {"speed" : 1,#the distance that the creature can move per step i time
                                "maximum view dist squared" : 1,#the maximum distance that the creature can see, squared
                                 "size can eat" : 0,#the biggest size of creature that this creature can eat, as a ratio
                                 "carnivorous":0,#if the creature can eat other creatures
                                 "number of offspring" : 1,#the number of offspring that will be had by the creature when it has offspring
                                 "time to grow up" : 100,#the number of steps in time it will take for the creature to be able to move
                                 "energy per unit size" : 100,#the amount of energy that a different creature will gain when eating this creature. this should probably be fixed and not here.
                                 "energy per distance moved" : 100,#also the amount of energy that will be used by the creature when it is moving
                                 "lifespan" : 100,#the number of steps in time after which the creature will die of old age
                                 "camouflage" : 0,#the chance that another creature won't see this animal. this includes mates
                                 "can recognise predators": 0,#if the creature can see predators, and therefore run away
                                 "can eat poison" : 0,#if the creature can eat poisonous plants
                                 "can see poison" : 0,#if the creature can see poisonous plants so it knows not to eat them
                                 "chance to have offspring" : 0#1/ the probability that an offspring will be had at a given opportunity
                                }
        self.newGeneration(characteristics, 1)
        pass

    def newGeneration(self, characteristics, size):
        #called by the server manager when the player responds with the characteristics they want
        #contains the processes so that the characteristics and size arrays are updated with the new characteristics

        self.size.append(size)
        self.characteristics.append(characteristics)
        self.characteristics.append(characteristics)

    def creatureIsKilled(self, creature):
        #removes the creature from creatures and adds it to the family tree
        self.familytree[creature.ID] = creature.offspring#this will likely need to be modified when the algorithm for displaying the family tree is implemented, or removed if it turns out that implemting a family tree is not practical in terms of processing time





class Ghost(Player):
    #the class so the player can spectate after they are extinct.
    #does not need any difference than parent class for now, but separate to allow for change.
    pass