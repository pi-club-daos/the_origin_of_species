class Game:
    def __init__(self):
        self.state#starting, running, finished
        self.players#a list of all the players(instances of the species class) in the game
        self.size
        self.items#a list of all the instances of the item class to iterate through when
        self.map#the map the game takes place in. A grid of a fixed size with random spaces that are not traversable. a 2d array of 1s and 0s
        self.chat#the global chat for the game
        self.time#the number of ticks since the beginning of the game
        self.tickSpeed
        #tick needs to be called in a seperate thread and recalled every 1/tickspeed seconds


    def updateChat(self):
        #a function so that items and species can update the chat when events happen. This is only for global events and messages.
        pass

    def addSpecies(self):
        #a function to add new players.
        pass

    def speciesIsDead(self):
        #does the appropriate processes when a species dies, including updating the players profile
        pass

    def tick(self):
        #this increases the time and tells every item to make decisions, then tells every item to act on the decisions
        pass

    def pathFind(self, loc1, loc2):
        #this function finds a path between two points and returns the path as a tuple
        pass



#the base class for all the different items/creatures that can exist in the game
class Item:
    def __init__(self):
        self.location#this is the location of the item on the map
        self.game#this is the instance of the game class that the item belongs to. it allows the item to tell the game class to do certain things i.e. if a creature has offspring, a plant is eaten
        self.size#this is the size of the item, important for eating

    def isInSight(self, playerLoc, playerRad):
        #this function checks if the item is visible by the player in playerLoc.
        pass

    def interestingCharacteristics(self):
        #this function returns the characteristics that affect the decisions that another item might take
        pass

    def eaten(self):
        # this function does the neccessary processes for if the creature is eaten. It will only be called by the creature that ate it
        pass



class Creature(Item):
    def __init__(self):
        Item.__init__(self)
        self.name#a randomly generated name for the creature
        self.age#the age of the item. This doesn't matter for plants. Age is the number of ticks since the item was created.
        self.species#the player who owns this creature
        self.characteristics#the characteristics of the creature stored in a dictionary with their state i.e. for size this would be the size as a number
        self.energy#the current energy of the creature. If this reaches zero the creature will die. It decreases with time and movement and increases by eating
        self.offspring#this is a list of the offspring of this creature. This enables the family tree to be created
        self.generation#the generation that this creature belongs to. Used by the creature class to decide if the player needs to decide new characteristics
        self.minPointsEnergy#the amount of energy required to gain a point when move is called

    def calculateMove(self, destination):
        #this function calculates the move for the creature. It will use pathfinding, and return the space that the player should move to based on the speed of the creature
        pass

    def move(self):
        #this function moves the creature based on the move from calculateMove. all creatures should be moved at the same time after decisions have all been made. The creatures energy should decrease more if it moves but should always be decreased here. The species points should increase if it has energy over minpointsenergy
        pass

    def haveOffspring(self):
        #this function does the neccessary processes for if the creature wants to have offspring, including prompting the player to make decisions if it is the first offspring of its generation
        pass

    def eat(self, item):
        #this function does the necessary processes for if the creature eats something. the amount of energy added should be decided by the size of the item
        pass

    def getInformation(self):
        #this function queries the isInSight of every item and returns a list of all that return true, along with the distance
        pass

    def makeDecisions(self):
        #this function makes decisions based on its characteristics and the interesting and based on the closest items first. As soon as one decision is made it will be done with this function.
        pass

    def eaten(self):
        # this function does the neccessary processes for if the creature is eaten. It will only be called by the creature that ate it
        pass

    def dead(self):
        #this function does the necessary processes for if the creature dies
        pass


class Plant(Item):
    def __init__(self):
        Item.__init__(self)
        self.poisonous

    def eaten(self):
        # this function does the neccessary processes for if the creature is eaten. It will only be called by the creature that ate it
        pass


class Species:
    def __init__(self):
        self.creatures#a list of all the living creatures in the species
        self.familytree#a tree of all the dead creatures
        self.chat#a chat containing all of the events specific to this species
        self.ID#the ID of this species that the player who is controlling this species needs to make actions
        self.characteristics#a list of the characteristics of each generation
        self.points#the points of the species, used to purchase new characteristics. Characteristics cost more the more creatures there are

    def addOffspring(self):
        #adds a new offspring and tells the player they need to specify the characteristics of the next generation if necessary
        pass

    def newGeneration(self):
        #called by the server manager when the player responds with the characteristics they want
        #contains the processes so that 