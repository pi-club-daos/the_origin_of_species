this is a game created by Thomas Chernaik that is a multiplayer strategy game based on the idea of evolution.
each player controls a species and decides the characteristics for each generation of that species based on points earned by the survival of their species. 
The ultimate goal is to be the last species left standing.

TODO:

finish serverManager

finish certain functions in game.py that i just haven't been bothered to do yet.

sort out the game so that it ends when there is one species left

sort out the game so the player can continue to spectate after they have died. the likely way to do this is by creating a ghost species class with nothing but the ability to read global chat and send messages.

finish functions which interact with server manager in game.py

start and finish flask server

start and finish python client(for testing)

start and finish web client

restructure server slightly so that it is possible to request the location, species and name of every living creature(only needed for unity client, but should be finished as part of coursework). this may not be neccesary as there is already a list of all of the items in the game, all of which know their species, so unless I need some information that i cannot think of now or it is too inefficient to acquire the locations like this nothing will need to be done.

start and finish unity client(long term, not part of coursework)
