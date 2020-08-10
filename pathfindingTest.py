from collections import deque
"""
written using this as a source for how to implement the algorithm in python:
https://medium.com/@nicholas.w.swift/easy-a-star-pathfinding-7e6689c7f7b2

also used this website for information 
http://theory.stanford.edu/~amitp/GameProgramming/Heuristics.html
"""
class Node:

    def __init__(self, parent=None, pos=None):
        self.parent = parent
        self.pos = pos

        self.f = 0
        self.g = 0
        self.h = 0

    def __eq__(self, other):
        return self.pos == other.pos

def astar(grid, start, end):
    start = Node(parent=None, pos=start)#creates a node for the start point
    end = Node(parent=None, pos=end)#creates a node for the end point
    open = deque()
    closed = deque()
    open.append(start)#adds the start node to the open list
    while len(open) > 0:
        current = open[0]
        current_index = 0
        index = 0
        #makes current the item in open with the lowest f value
        for item in open:
            if item.f < current.f:
                current = item
                current_index = index
            index += 1
        closed.append(open.pop(current_index))#takes current out of open and puts it in closed

        #sees if we have found end and then takes the path backwards and reverses the path to find the correct route
        if current == end:
            path = deque()
            while current:
                path.append(current.pos)
                current = current.parent
            path.reverse()
            return path

        children = deque()
        for new_pos in [(-1, 0), (0, -1), (0, 1), (1, 0)]:#these are the adjacent squares vertically and horizontally
            pos = (current.pos[0] + new_pos[0], current.pos[1] + new_pos[1])
            if pos[0] > len(maze)-1 or pos[0] < 0 or pos[1] > len(maze[0])-1 or pos[1] < 0:#if the position is out of the maze continue to the next iteration
                continue


            new = Node(parent=current, pos=pos)
            children.append(new)
            for child in children:
                for node in closed:#if this square is already in closedList i.e is already in the path continue
                    if child == closed:
                        continue
                child.g = current.g + 1 + maze[pos[0]][pos[1]]) * 10#this encourages the algorithm to not walk over the terrain however it can if it is neccessary. This means that generally it will walk around however if a player is surrounded by terrain they won't be trapped.
                child.h = (child.pos[0] - end.pos[0])+(child.pos[1] - end.pos[1])#many examples i have found online use pythagoras to find the distance however this requires a square root which is slow. because we are working on a grid and you can't move diagonally, this works just as well as it is the minimum distance possible.
                child.f = child.g + child.h
                for node in open:#don't bother with this if it is already in open with a lower g because that means there is a faster way to get to child
                    if child == node:
                        if child.g > open.g:
                            continue
                        else:
                            del(node)

                open.append(child)
    raise Exception("could not traverse from start to end")