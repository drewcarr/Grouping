import random
import heapq
import math

from graphics import *

COLORS = ["blue", "red", "yellow", "orange", "purple", "green"]

windowWidth = 700
windowHeight = 700

width = 20
height = 20

groups_num = 6
density = 10

# 1 / anomaly = % random
anomaly = 100

points = []
groups = []

win = GraphWin("Grouping", windowWidth, windowHeight)
win.setCoords(-1, -1, width, height)

def main():
    while(1):
        updatePoints()

    win.getMouse() # Pause to view result
    win.close()    # Close window when done

def init():
    for i in range(0, width):
        list = [0] * height
        points.append(list)

    for g in range(0, groups_num):
        group = []
        for d in range(0, density):
            # create random coordinate
            # update in points with g
            # create shape and add to group
            '''
            if (g == 0):
                x = 0
                y = 0
            else:
                x = width - 1
                y = height - 1
            '''
            x = random.randint(0, width - 1)
            y = random.randint(0, height - 1)
            while (points[x][y] != 0):
                x = random.randint(0, width - 1)
                y = random.randint(0, height - 1)

            points[x][y] = g + 1
            c = Circle(Point(x,y), 0.5)
            c.setFill(COLORS[g])
            c.draw(win)
            group.append(c)
        groups.append(group)

def getMove(g, color):
    p = g.getCenter()
    x = int(p.getX())
    y = int(p.getY())
    possibleMoves = []
    possibleMoves.append((x, y))
    if (x > 0):
        if (points[x - 1][y] == 0):
            possibleMoves.append((x - 1, y))
        if (y > 0):
            if (points[x - 1][y - 1] == 0):
                possibleMoves.append((x - 1, y - 1))
        if (y < height - 1):
            if (points[x - 1][y + 1] == 0):
                possibleMoves.append((x - 1, y + 1))
    if (x < width - 1):
        if (points[x + 1][y] == 0):
            possibleMoves.append((x + 1, y))
        if (y > 0):
            if (points[x + 1][y - 1] == 0):
                possibleMoves.append((x + 1, y - 1))
        if (y < height - 1):
            if (points[x + 1][y + 1] == 0):
                possibleMoves.append((x + 1, y + 1))
    if (y > 0):
        if (points[x][y - 1] == 0):
            possibleMoves.append((x, y - 1))
    if (y < height - 1):
        if (points[x][y + 1] == 0):
            possibleMoves.append((x, y + 1))

    # update points
    points[x][y] = 0

    # Used to create randomness
    if (random.randint(0, anomaly) == 0):
        print("Random move")
        i = random.randint(0, len(possibleMoves) - 1)
        points[possibleMoves[i][0]][possibleMoves[i][1]] = color + 1
        return (possibleMoves[i][0] - x, possibleMoves[i][1] - y)

    optimalMove = getOptimalMove(possibleMoves, color)
    points[optimalMove[0]][optimalMove[1]] = color + 1
    return (optimalMove[0] - x, optimalMove[1] - y)

def getOptimalMove(possibleMoves, color):
    weightedMoves = [(0,x,y) for (x, y) in possibleMoves]
    for c, group in enumerate(groups):
        for g in group:
            point = g.getCenter()
            x = point.getX()
            y = point.getY()
            for i, move in enumerate(weightedMoves):
                dist = (move[1] - x)*(move[1] - x) + (move[2] - y)*(move[2] - y)
                if (c == color):
                    weightedMoves[i] = (move[0] + dist, move[1], move[2])
                else:
                    weightedMoves[i] = (move[0] - dist / groups_num, move[1], move[2])
    heapq.heapify(weightedMoves)
    return (weightedMoves[0][1], weightedMoves[0][2])

def updatePoints():
    for i, group in enumerate(groups):
        for g in group:
            move = getMove(g, i)
            g.move(move[0], move[1])

init()
main()
