import game
mygame = game.Game(3, 100)
mystr = "P1 100 100"
for i in mygame.map:
    for j in i:
        mystr += " " + str(j)
with open("test.pbm", "w+") as myfile:
    myfile.write(mystr)