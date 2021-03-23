from collections import deque
import heapq
import mylogging
"""
written using this as a source for how to implement the algorithm in python:
https://medium.com/@nicholas.w.swift/easy-a-star-pathfinding-7e6689c7f7b2

also used this website for information 
http://theory.stanford.edu/~amitp/GameProgramming/Heuristics.html
"""
class Node:
    @mylogging.log
    def __init__(self, parent=None, pos=None):
        self.parent = parent
        self.pos = pos

        self.f = 0
        self.g = 0
        self.h = 0

    @mylogging.log
    @property
    def h(self):
        return self.__h

    @mylogging.log
    @h.setter
    def h(self, value):
        self.__h = value

    @mylogging.log
    @property
    def g(self):
        return self.__g

    @mylogging.log
    @g.setter
    def g(self, value):
        self.__g = value

    @mylogging.log
    @property
    def f(self):
        return self.__f

    @mylogging.log
    @f.setter
    def f(self, value):
        self.__f = value

    @mylogging.log
    def __eq__(self, other):
        return self.pos == other.pos

    @mylogging.log
    def __lt__(self, other):
        return self.f < other.f

    @mylogging.log
    def __le__(self, other):
        return self.f <= other.f

    @mylogging.log
    def __gt__(self, other):
        return self.f > other.f

    @mylogging.log
    def __ge__(self, other):
        return self.f >= other.f

@mylogging.log
def astar(grid, start, end):
    if grid[start[0]][start[1]] or grid[end[0]][end[1]]:#if either the start or the end are in an intraversable place then just do a direct route.
        return directRoute(start,end)
    start = Node(parent=None, pos=start)#creates a node for the start point
    end = Node(parent=None, pos=end)#creates a node for the end point
    open = []
    closed = []
    heapq.heappush(open, start)#adds the start node to the open list
    count = 0
    while len(open) > 0:
        count +=1
        current = heapq.heappop(open)
        closed.append(current)
        #sees if we have found end and then takes the path backwards and reverses the path to find the correct route
        if current == end or count == 500:
            path = deque()
            while current:
                path.append(current.pos)
                current = current.parent
            path.reverse()
            return list(path)

        children = deque()
        for new_pos in [(-1, 0), (0, -1), (0, 1), (1, 0)]:#these are the adjacent squares vertically and horizontally
            pos = (current.pos[0] + new_pos[0], current.pos[1] + new_pos[1])
            if pos[0] > (len(grid)-1) or pos[0] < 0 or pos[1] > (len(grid[0])-1) or pos[1] < 0 or grid[pos[0]][pos[1]]:#if the position is out of the maze continue to the next iteration
                continue
            new = Node(parent=current, pos=pos)
            children.append(new)
        for child in children:

            if child in closed:
                continue
            child.g = current.g + 1
            child.h = abs(end.pos[0] - child.pos[0])+abs(end.pos[1] - child.pos[1])#many examples i have found online use pythagoras to find the distance however this requires a square root which is slow. because we are working on a grid and you can't move diagonally, this works just as well as it is the minimum distance possible.
            child.f = child.g + child.h
            if child in open:
                new_child = open[open.index(child)]
                if child.g > new_child.g:
                    new_child.g = child.g
                    new_child.parent = child.parent
                    new_child.f = child.f
                    continue
            heapq.heappush(open, child)
    raise Exception("could not traverse from start to end")

@mylogging.log
def directRoute(start, end):
    xDist = end[0] - start[0]
    yDist = end[1] - start[1]
    xSign = (xDist >> 31)*(2) + 1
    ySign = (yDist >> 31)*(2) + 1
    route = []
    for i in range(abs(xDist)+1):
        route.append([start[0] + xSign * i, start[1]])
    for j in range(abs(yDist)+1):
        route.append([start[0] + xSign*i, start[1] + ySign*j])
    return route