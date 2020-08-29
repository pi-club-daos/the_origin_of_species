import random
#the first-names.txt file is from https://raw.githubusercontent.com/dominictarr/random-name/master/first-names.txt
def generateName():
    #https://stackoverflow.com/questions/10819911/read-random-lines-from-huge-csv-file-in-python
    #this function chooses a random name from a text file using the technique in the link above
    length = 30193#this is probably correct i got it from a character counter website but i am subtracting 20 to make sure it isn't in the last line
    offset = random.randrange(length)
    f = open("first-names.txt")#open the file
    f.seek(offset)#go to the offset
    f.readline()#go to the next line because the offset is probably in the middle of this one
    return f.readline()

