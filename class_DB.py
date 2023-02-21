#################################################
# The Doomsday Battle(112 Term Project)
#################################################
import math
import random

class IsoRec:
    def __init__(self,isoX,isoY,recWidth,recHeight,fill):
        self.isoX = isoX
        self.isoY = isoY
        self.recWidth = recWidth
        self.recHeight = recHeight
        self.ploygon = ((isoX-recWidth/2,isoY+recHeight/2),#left
        (isoX,isoY+recHeight),#down
        (isoX+recWidth/2,isoY+recHeight/2),#right
        (isoX,isoY))#up

class Wall:
    def __init__(self,rows,cols):
        self.rows = rows
        self.cols = cols
        # self.absx0 = x0
        # self.absx1 = x1
        # self.absy0 = y0
        # self.absy1 = y1

    # def getWallBounds(self):
    #     return (self.absx0, self.absy0, self.absx1, self.absy1)

class Wormhole:
    def __init__(self,row,col,cx,cy,size):
        self.row = row
        self.col = col
        self.cx = cx
        self.cy = cy
        self.size = size

    def getWallBounds(self):
        #return (self.absx0, self.absy0, self.absx1, self.absy1)
        pass

    def getDestination(self,rows,cols):
        dRow = int(random.randint(1, rows-1))
        dCol = int(random.randint(1, cols-1))
        return (dRow,dCol)

    def updateDestination(self,rows,cols):
        dRow = int(random.randint(1, rows-1))
        dCol = int(random.randint(1, cols-1))
        return (dRow,dCol)
    
    def update(self):
        pass

# class Node from https://medium.com/@nicholas.w.swift/easy-a-star-pathfinding-7e6689c7f7b2
class Node():
    def __init__(self, parent, position):
        self.parent = parent
        self.position = position

        self.distance = 0
        self.heuristic = 0
        self.cost = 0

    def __eq__(self, other):
        return (isinstance(other, Node) and self.position == other.position)

    def __repr__(self):
        return f"Node at {self.position} with f={self.cost}"

    def __hash__(self):
        return hash((self.parent, self.position, self.distance, self.heuristic, self.cost)) 


#################################################
# Boids and flocking simulation 
#################################################
# boids from https://medium.com/@sowmyab/implementing-boids-in-python-ede6e2ad652d
# Vector functions, playerCohesion and playerSeparation from
# https://github.com/RamenBucket/Term-Project-112

def getAngle(x, y):
    # if the line is vertial
    if x == 0 and y <= 0:
        return 3 * math.pi/2
    elif x == 0 and y >= 0:
        return math.pi/2 
    # other cases for arctan function
    elif x >= 0 and y >= 0:
        return math.atan(abs(y/x))
    elif x <= 0 and y >= 0:
        return math.pi/2 + (math.pi/2 - math.atan(abs(y/x)))
    elif x <= 0 and y <= 0:
        return math.pi + math.atan(abs(y/x))
    else:
        return 3*(math.pi/2) + (math.pi/2 - math.atan(abs(y/x)))

# returns direction vector given angle in radians
def getVector(angle):
    return (math.cos(angle), math.sin(angle))

def addVector(v1, v2):
    return [v1[0] + v2[0], v1[1] + v2[1]]

def subtractVector(v1, v2):
    return [v1[0] - v2[0], v1[1] - v2[1]]

def addVectorWrapAround(v1, v2, w, h):
    return [(v1[0] + v2[0]) % w, (v1[1] + v2[1]) % h]

def multiplyVector(v, n):
    return [v[0] * n, v[1] * n]

def divideVector(v, n):
    return [v[0] / n, v[1] / n]

def distance(p1, p2):
    return ((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)**0.5

# flocking from https://thecodingtrain.com/CodingChallenges/124-flocking-boids
class Boid(object):
    def __init__(self, pos, vel, acc):
        self.pos = pos
        self.vel = vel
        self.acc = acc
        self.maxAllignForce = .02
        self.maxCohesionForce = .02
        self.maxSeparationForce = .02
        self.maxSpeed = 2

    def __eq__(self, other):
        return isinstance(other, Boid) and (self.pos == other.pos and
                                            self.vel == other.vel and
                                            self.acc == other.acc and
                                            self.maxAllignForce == other.maxAllignForce and
                                            self.maxCohesionForce == other.maxCohesionForce and
                                            self.maxSpeed == other.maxSpeed)

    def allign(self, boids):
        perceptionRadius = 100
        steering = [0, 0]
        total = 0
        for boid in boids:
            if boid != self and distance(self.pos, boid.pos) < perceptionRadius:
                steering = addVector(steering, boid.vel)
                total += 1
        if total > 0:
            steering = divideVector(steering, total) # divide by total to get average
            steering = multiplyVector(getVector(getAngle(steering[0], steering[1])), self.maxSpeed)
            steering = subtractVector(steering, self.vel) # subtracting
            # limits the magnitude of alignment
            if distance([0,0], steering) > self.maxAllignForce:
                steering = multiplyVector(getVector(getAngle(steering[0], steering[1])), self.maxAllignForce)
        return steering

    def separation(self, boids):
        perceptionRadius = 100
        steering = [0, 0]
        total = 0
        for boid in boids:
            if boid != self and distance(self.pos, boid.pos) < perceptionRadius:
                diff = subtractVector(self.pos, boid.pos)
                diff = divideVector(diff, distance(self.pos, boid.pos))
                steering = addVector(steering, diff)
                total += 1
        if total > 0:
            steering = divideVector(steering, total) # divide by total
            steering = multiplyVector(getVector(getAngle(steering[0], steering[1])), self.maxSpeed)
            steering = subtractVector(steering, self.vel) # subtracting
            # limits the magnitude of alignment
            if distance([0,0], steering) > self.maxSeparationForce:
                steering = multiplyVector(getVector(getAngle(steering[0], steering[1])), self.maxSeparationForce)
        return steering

    def playerSeparation(self, player):
        maxSeparationForcePlayer = .03
        perceptionRadius = 200
        steering = [0, 0]
        total = 0
        separationWeight = 5
        if distance(self.pos, player.pos) < perceptionRadius:
            diff = multiplyVector(subtractVector(self.pos, player.pos), separationWeight)
            diff = multiplyVector(divideVector(diff, distance(self.pos, player.pos)), separationWeight)
            steering = addVector(steering, diff)
            total += 1 * separationWeight
        if total > 0:
            steering = divideVector(steering, total) # divide by total
            steering = multiplyVector(getVector(getAngle(steering[0], steering[1])), self.maxSpeed)
            steering = subtractVector(steering, self.vel) # subtracting
            # limits the magnitude of alignment
            if distance([0,0], steering) > maxSeparationForcePlayer:
                steering = multiplyVector(getVector(getAngle(steering[0], steering[1])), maxSeparationForcePlayer)
        return steering

    def playerCohesion(self, player):
        maxCohesionForcePlayer = .01
        perceptionRadius = 500
        steering = [0, 0]
        total = 0
        if distance(self.pos, player.pos) < perceptionRadius:
            steering = addVector(steering, player.pos)
            total += 1
        if total > 0:
            steering = divideVector(steering, total) # divide by total
            steering = subtractVector(steering, self.pos)
            steering = multiplyVector(getVector(getAngle(steering[0], steering[1])), self.maxSpeed)
            steering = subtractVector(steering, self.vel) # subtracting
            # limits the magnitude of alignment
            if distance([0,0], steering) > maxCohesionForcePlayer:
                steering = multiplyVector(getVector(getAngle(steering[0], steering[1])), maxCohesionForcePlayer)
        return steering

    def cohesion(self, boids):
        perceptionRadius = 100
        steering = [0, 0]
        total = 0
        for boid in boids:
            if boid != self and distance(self.pos, boid.pos) < perceptionRadius:
                steering = addVector(steering, boid.pos)
                total += 1
        if total > 0:
            steering = divideVector(steering, total) # divide by total
            steering = subtractVector(steering, self.pos)
            steering = multiplyVector(getVector(getAngle(steering[0], steering[1])), self.maxSpeed)
            steering = subtractVector(steering, self.vel) # subtracting
            # limits the magnitude of alignment
            if distance([0,0], steering) > self.maxCohesionForce:
                steering = multiplyVector(getVector(getAngle(steering[0], steering[1])), self.maxCohesionForce)
        return steering

    def flock(self, boids, player=None):
        alignment = self.allign(boids)
        cohesion = self.cohesion(boids)
        separation = self.separation(boids)
        #asteroidSeparation = self.asteroidSeparation(asteroids)
        
        self.acc = addVector(self.acc, alignment)
        self.acc = addVector(self.acc, cohesion)
        self.acc = addVector(self.acc, separation)
        #self.acc = addVector(self.acc, asteroidSeparation)
        if player != None:
            playerSeparation = self.playerSeparation(player)
            playerCohesion = self.playerCohesion(player)
            self.acc = addVector(self.acc, playerSeparation)
            self.acc = addVector(self.acc, playerCohesion)

    def update(self, app):
        # update position
        self.pos = addVectorWrapAround(self.pos, self.vel, app.absWidth, app.absHeight)
        self.pos = addVector(self.pos, self.vel)
        # update velocity
        self.vel = addVector(self.vel, self.acc)
        if distance([0, 0], self.vel) > self.maxSpeed:
            self.vel = multiplyVector(getVector(getAngle(self.vel[0], self.vel[1])), self.maxSpeed)
        self.acc = [0, 0]

    def show(self, app, canvas):
        pass
        # r = 7
        # cx, cy = self.pos
        # vx, vy = self.vel
        # canvas.create_oval(cx-r, cy-r, cx+r, cy+r, fill = 'yellow')
        # shape = [(cx, cy-r), (cx+r, cy), (cx, cy+r), (cx-r, cy)]
        #canvas.create_polygon(shape, fill = 'white', outline = 'black')
        # x1 = cx + r * math.cos(self.angle)
        # x2 = cy + r * math.sin(self.angle)
        # canvas.create_line(cx,cy, vx,vy,
        #                     fill='red', arrow='last', 
        #                     arrowshape=(12.8,16,4.8), width=2)