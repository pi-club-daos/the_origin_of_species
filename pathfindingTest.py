import pathfinding, noise, random, time


def generateMap(mapsize):
    # generate the map using simplex noise so it looks somewhat realistic if presented in a graphical interface. this should also mean that there are no open spaces that are shut off
    octaves = 1
    freq = 0.15 * mapsize  # this means the map will not change based on mapsize
    seed = random.randint(-1000000,
                          1000000)  # if you put a random number generator in a generator it generates a different number each time and becomes random noise so it must be here instead
    map = [[1 if noise.snoise2(x / freq, y / freq, octaves, base=(seed)) > 0.5 else 0 for y in range(mapsize)] for x in
           range(mapsize)]  # for whatever reason the base parameter of this function must be less than 1 million
    return map
size = 500
map = generateMap(size)
timer = time.time()
path = pathfinding.astar(map, (50,30), (60,60))
for i in path:
    map[i[1]][i[0]] = "2"
with open("test.pgm", "w+") as myfile:
    string = f"P2 {len(map[0])} {len(map)} 2 "
    for i in map:
        string += " ".join([str(j) for j in i]) + "\n"
    myfile.write(string)
print(time.time() - timer)
print(path)