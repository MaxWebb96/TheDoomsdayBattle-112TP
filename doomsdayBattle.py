#################################################
# The Doomsday Battle(112 Term Project)
# Verson: 1.3
# Last Updated: Dec 5
# Autor: Zain Hao (andrew id: xingh)
#################################################

import math, copy, random
from class_DB import *
from cmu_112_graphics import *
from otherMode import *

#################################################
# Game Mode
#################################################

#https://www.cs.cmu.edu/~112/notes/notes-animations-part4.html#usingModes

def gameDimensions():
    cellWidth = 30
    cellHeight = 30
    rows = 60
    cols = 80
    # isometric
    # tileHeight = 30
    # tileWidth = 30
    margin = 30
    return (rows, cols, cellWidth, cellHeight, margin)

def getPlayerBounds(app):
    # returns absolute bounds, not taking scrollX into account
    (x0, y0) = (app.playerX-app.playerWidth/2,app.playerY-app.playerHeight/2)
    (x1, y1) = (app.playerX+app.playerWidth/2,app.playerY+app.playerHeight/2)
    return (x0, y0, x1, y1)
    
def generateWalls(app,count):
    i = 0
    while i < count:
        row = int(random.randint(2, app.rows-3))
        col = int(random.randint(2, app.cols-3))
        # safe zone
        safeRange = 10
        if not app.Blocks[row][col] and not(2<=row<=safeRange and 2<=col<=safeRange):
            i += 1
            #rows,cols = generateSingleWall(app,row,col,3)
            wall = Wall(row,col)
            app.walls.add(wall)
            # for i in range(len(wall.rows)):
            app.Blocks[wall.rows][wall.cols] = True
            app.Blocks[wall.rows+1][wall.cols] = True
            app.Blocks[wall.rows+2][wall.cols] = True
            
def generateSingleWall(app,row,col,length):
    rows = []
    cols = []
    if row+col%2 ==0:
        range1 = col-length//2
        for col1 in range(range1,range1+length):
            cols.append(col1)
            rows.append(row)
    else:
        range1 = row-length//2
        for row1 in range(range1,range1+length):
            cols.append(col)
            rows.append(row1)
    return rows,cols

def drawWalls(app,canvas):
    sx = app.scrollX
    sy = app.scrollY
    for wall in app.walls:
            (x0, y0, x1, y1) = getCellBounds(app,wall.rows,wall.cols)
            (x00, y00, x11, y11) = getCellBounds(app,wall.rows+2,wall.cols)
            fill = "gray"
            canvas.create_rectangle(x0-sx, y0-sy, x11-sx, y11-sy, fill=fill)

def generateWormhole(app,count):
    i = 0
    while i < count:
        row = int(random.randint(1, app.rows-2))
        col = int(random.randint(1, app.cols-2))
        (x0,y0,x1,y1) = getCellBounds(app,row,col)
        cx = (x0+x1)/2
        cy = (y0+y1)/2
        size = random.randint(20, 50)
        wormhole = Wormhole(row,col,cx,cy,size)
        if not app.Blocks[row][col]:
            app.wormholes.add(wormhole)
            i += 1

def putWormhole(app,x,y):
    (row,col) = getCell(app,x, y)
    (x0,y0,x1,y1) = getCellBounds(app,row,col)
    cx = (x0+x1)/2
    cy = (y0+y1)/2
    size = random.randint(20, 50)
    wormhole = Wormhole(row,col,cx,cy,size)
    if not app.Blocks[row][col]:
            app.wormholes.add(wormhole)
    
def drawWormholes(app,canvas):
    sx = app.scrollX
    sy = app.scrollY
    for wormhole in app.wormholes:
        # (x0, y0, x1, y1) = getCellBounds(app, wormhole.row, wormhole.col)
        cx = wormhole.cx
        cy = wormhole.cy
        size = wormhole.size
        # fill = "green"
        # canvas.create_oval(cx-size-sx, cy-size-sy, 
        #                 cx+size-sx, cy+size-sy, fill=fill)
        wormhole1 = app.scaleImage(app.image_wormhole,size*0.02)
        canvas.create_image(cx-sx, cy-sy, 
                        image=ImageTk.PhotoImage(wormhole1))

def getWormholeFalling(app):
    for wormhole in app.wormholes:
        if distance(app.playerX,app.playerY,wormhole.cx,wormhole.cy) <= wormhole.size*1.5:
            return wormhole

def checkForFalling(app):
    wormhole = getWormholeFalling(app)
    if wormhole != None:
        (row,col) = wormhole.getDestination(app.rows,app.cols)
        while app.Blocks[row][col]:
            (row,col) = wormhole.getDestination(app.rows,app.cols)

        (x0,y0,x1,y1) = getCellBounds(app,row,col)
        dX = x0 - app.playerX
        dY = y0 - app.playerY
        app.playerX += dX
        app.playerY += dY
        app.scrollX -= dX
        app.scrollY -= dY
        app.wormholes.remove(wormhole)
        generateWormhole(app,1)
        app.score += 200

def getFlockTouch(app):
    for boid in app.flock:
        if distance(app.playerX,app.playerY,boid.pos[0],boid.pos[1]) <= 20:
            return boid

def checkForTouch(app):
    boid = getFlockTouch(app)
    if boid != None:
        app.flock.remove(boid)
        removeHealth(app,50)

def boundsIntersect(app, boundsA, boundsB):
    # return l2<=r1 and t2<=b1 and l1<=r2 and t1<=b2
    (ax0, ay0, ax1, ay1) = boundsA
    (bx0, by0, bx1, by1) = boundsB
    return ((ax1 >= bx0) and (bx1 >= ax0) and
            (ay1 >= by0) and (by1 >= ay0))

def makePlayerVisible(app):
    # scroll to make player visible as needed
    if (app.playerX < app.scrollX + app.scrollMargin):
        app.scrollX = app.playerX - app.scrollMargin
    if (app.playerX > app.scrollX + app.width - app.scrollMargin):
        app.scrollX = app.playerX - app.width + app.scrollMargin
    if (app.playerY < app.scrollY + app.scrollMargin):
        app.scrollY = app.playerY - app.scrollMargin
    if (app.playerY > app.scrollY + app.height - app.scrollMargin):
        app.scrollY = app.playerY - app.height + app.scrollMargin

def addVector(v1, v2):
    return [v1[0] + v2[0], v1[1] + v2[1]]

def readPlayerAbsVel(app):
    return roundHalfUp((app.playerVel[0]**2 + app.playerVel[1]**2)**0.5)

def accPlayer(app,acc):
    if readPlayerAbsVel(app) <= app.maxAbsVel - 1:
        app.playerVel = addVector(app.playerVel,app.playerAcc)

        # app.playerVel[0] = roundHalfUp(app.playerVel[0])
        # app.playerVel[1] = roundHalfUp(app.playerVel[1])
    app.playerAcc = acc

def slowDown(app):
    if readPlayerAbsVel(app) >= 1:
        app.playerVel[0] = int(app.playerVel[0] * 0.6)
        app.playerVel[1] = int(app.playerVel[1] * 0.6)

def movePlayer(app):
    accPlayer(app,app.playerAcc)
    currentPos = (app.playerX,app.playerY)
    (nextX,nextY) = addVector(currentPos,app.playerVel)
        # nextX = app.playerX + app.playerDir[0]*app.playerSpeed
        # nextY = app.playerY + app.playerDir[1]*app.playerSpeed
    nextX = roundHalfUp(nextX)
    nextY = roundHalfUp(nextY)
    if isMovable(app,nextX,nextY):
            app.playerX = nextX
            app.playerY = nextY
    else: app.playerVel = (0,0)
    checkForFalling(app)
    checkForTouch(app)
    makePlayerVisible(app)

def flashPlayer(app):
    currentPos = (app.playerX,app.playerY)
    flashDis = 200
    flashVec = (app.playerAcc[0]*flashDis,app.playerAcc[1]*flashDis)
    (nextX,nextY) = addVector(currentPos,flashVec)
        # nextX = app.playerX + app.playerDir[0]*app.playerSpeed
        # nextY = app.playerY + app.playerDir[1]*app.playerSpeed
    nextX = roundHalfUp(nextX)
    nextY = roundHalfUp(nextY)
    if isMovable(app,nextX,nextY):
            app.playerX = nextX
            app.playerY = nextY
    #else: app.playerVel = (0,0)
    checkForFalling(app)
    makePlayerVisible(app)

def applyFriction(app):
    pass

def isMovable(app,x,y):
    nextX = x
    nextY = y
    (row,col) = getCell(app,nextX,nextY)
    return 0<=row<app.rows and 0<=col<app.cols and not app.Blocks[row][col]

def removeHealth(app,amount):
    app.health -= amount
    if app.health <= 0:
        app.isGameOver = True
        app.mode = 'endScreenMode'
    
def drawPlayer(app,canvas):
    sx = app.scrollX
    sy = app.scrollY
    (x0, y0, x1, y1) = getPlayerBounds(app)
    (cx,cy) = ((x0+x1)/2,(y0+y1)/2)
    # canvas.create_oval(x0 - sx, y0 - sy , x1 - sx, y1 - sy , 
    #                     fill="white", outline = 'black', width = 3)
    # canvas.create_image(cx - sx, cy - sy , 
    #                     image = ImageTk.PhotoImage(app.image_player))
    #sprite = rotateImage(app,sprite,180)
    #sprite = app.cSprites[app.spriteCounter]
    adjustPic = 21
    if app.cSprites == app.sprites_1:
        canvas.create_image(cx - sx, cy + adjustPic - sy, image=ImageTk.PhotoImage(app.cSprites[app.spriteCounter]))
    elif app.cSprites == app.sprites_2:
        canvas.create_image(cx - sx, cy -adjustPic- sy, image=ImageTk.PhotoImage(app.cSprites[app.spriteCounter]))
    elif app.cSprites == app.sprites_3:
        canvas.create_image(cx +adjustPic- sx, cy - sy, image=ImageTk.PhotoImage(app.cSprites[app.spriteCounter]))
    else:
        canvas.create_image(cx -adjustPic- sx, cy - sy, image=ImageTk.PhotoImage(app.cSprites[app.spriteCounter]))
    #canvas.create_rectangle(x0 - sx, y0 -sy,x1-sx,y1-sy,fill = None, outline = 'white')

def sizeChanged(app):
    makePlayerVisible(app)

def nextLevel(app):
    app.level += 1
    app.scoreLine *= 2

    app.playerX = app.scrollMargin
    app.playerY = app.scrollMargin
    
    app.dropletX  = app.width - app.margin
    app.dropletY  = app.height - app.margin
    app.dropletSpeed *= 1.5

    app.Blocks = [[False]*app.cols for row in range(app.rows)]
    app.walls = set()
    generateWalls(app, 20+app.level*20)

    app.flock = []
    initFlock(app,20+20*app.level)

#################################################
# Droplet_Hunter
#################################################
# https://www.cs.cmu.edu/~112/notes/notes-animations-part1.html#exampleGrids
# Gets row and col based on abs-x, y 
def getCell(app, x, y):
    rows, cols, cellWidth, cellHeight, margin = gameDimensions()
    row = int((y - app.margin) // cellHeight)
    col = int((x - app.margin) // cellWidth)
    return (row, col)

def getCellBounds(app, row, col):
    rows, cols, cellWidth, cellHeight, margin = gameDimensions()
    x0 = app.margin + col * cellWidth
    x1 = app.margin + (col+1) * cellWidth
    y0 = app.margin + row * cellHeight
    y1 = app.margin + (row+1) * cellHeight
    return (x0, y0, x1, y1)
    
# Droplet
# astar algo from:
# https://mat.uab.cat/~alseda/MasterOpt/AStar-Algorithm.pdf
# https://medium.com/@nicholas.w.swift/easy-a-star-pathfinding-7e6689c7f7b2
def astar(app, startval, endval):
    # Init start and end nodes, and lists
    start = Node(None, startval)
    end = Node(None, endval)
    openList = []
    closedList = set()
    openList.append(start)

    # Loop until you find end
    while len(openList) > 0:
        current = openList[0]
        bestNode = 0
        for i in range(len(openList)):
            if current.cost > openList[i].cost:
                current = openList[i]
                bestNode = i
        openList.pop(bestNode)
        closedList.add(current)
        if current == end:
            path = []
            tempcurrent = current
            while tempcurrent != None:
                path.append(tempcurrent.position)
                tempcurrent = tempcurrent.parent
            return path[::-1]
        children = []
        # children are adjacent nodes
        for (drow, dcol) in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
            row = current.position[0] + drow
            col = current.position[1] + dcol
            if (0 <= row < app.rows and 0 <= col < app.cols and 
                not app.Blocks[row][col]):
                #isMovable_Droplet(app, drow, dcol, row, col)): 
                new_node = Node(current, (row,col))
                children.append(new_node)

        for child in children:
            if child not in closedList:
                child.distance = current.distance + 1
                child.heuristic = ((child.position[0] - end.position[0]) ** 2) + ((child.position[1] - end.position[1]) ** 2)
                child.cost = child.distance + child.heuristic  
            if child not in openList:                    
                openList.append(child)

def isMovable_Droplet(app, drow, dcol, row, col):
    return False

def moveDroplet(app):
    dRow, dCol = getCell(app, app.dropletX, app.dropletY)
    pRow, pCol = getCell(app, app.playerX, app.playerY)
    start = (dRow, dCol)
    end = (pRow, pCol)
    #cal the path
    app.path = astar(app, start, end)
    if len(app.path) > 1:
        row, col = app.path[1]
        (x0, y0, x1, y1) = getCellBounds(app, row, col)
        app.targetX = (x0 + x1) //2
        app.targetY = (y0 + y1)//2

def handleDroplet(app):
    if distance(app.playerX, app.playerY, app.dropletX, app.dropletY) > 400:
        dropletSpeed = app.dropletSpeed * 2
    else:  dropletSpeed = app.dropletSpeed

    if distance(app.targetX, app.targetY, app.dropletX, app.dropletY) > 10:
        if app.targetX > app.dropletX:
            app.dropletX += dropletSpeed
        else: app.dropletX -= dropletSpeed
        if app.targetY > app.dropletY:
            app.dropletY += dropletSpeed
        else: app.dropletY -= dropletSpeed
    else: removeHealth(app,200)

def drawDroplet(app,canvas):
    sx = app.scrollX
    sy = app.scrollY
    # (x0, y0, x1, y1) = (app.dropletX-5,app.dropletY-5,
    #                     app.dropletX+5,app.dropletY+5)
    # canvas.create_oval(x0 - sx, y0 - sy , x1 - sx, y1 - sy , 
    #                     fill="orange", outline = 'black', width = 1)
    canvas.create_image(app.dropletX + 10 -sx, app.dropletY - sy,
                        image=ImageTk.PhotoImage(app.image_droplet))
    drawDropltTrack(app,canvas)

def drawDropltTrack(app,canvas):
    sx = app.scrollX
    sy = app.scrollY
    maxSize = 5
    for i in range(1,len(app.dropletTrack)-1):
        # draw oval
        ts = maxSize * 0.1 * i
        (cx,cy) = (app.dropletTrack[i][0],app.dropletTrack[i][1])
        canvas.create_polygon(cx- ts - sx, cy - sy, cx - sx, cy - ts - sy,
                             cx + ts - sx, cy - sy, cx - sx, cy + ts - sy,
                            fill="orange", outline = None, width = 1)
        # (x0, y0, x1, y1) = (app.dropletTrack[i][0]-trackSize,app.dropletTrack[i][1]-trackSize,
        #                  app.dropletTrack[i][0]+trackSize,app.dropletTrack[i][1]+trackSize)
        # canvas.create_oval(x0 - sx, y0 - sy , x1 - sx, y1 - sy , 
        #                 fill="orange", outline = None, width = 1)
        # draw line

        # (x0, y0, x1, y1) = (app.dropletTrack[i][0],app.dropletTrack[i][1],
        #                  app.dropletTrack[i+1][0],app.dropletTrack[i+1][1])
        # canvas.create_line(x0 - sx, y0 - sy , x1 - sx, y1 - sy , 
        #                 fill="silver", width = trackSize)


        
def updateDropletTrack(app):
    length = 10
    currentPos = (app.dropletX,app.dropletY)
    app.dropletTrack.append(currentPos)
    if len(app.dropletTrack) > length:
        app.dropletTrack.pop(0)

def drawBaseLine(app,canvas):
    # draw the base line
    lineY = app.height*0.8
    lineHeight = 10
    canvas.create_rectangle(0, lineY, app.width, lineY+lineHeight,fill="black")

def drawNavMap(app,canvas):
    # sx = app.scrollX
    # sy = app.scrollY
    
    cellWidth = 3
    cellHeight = 2
    oriX = app.width - 10 - app.cols*cellWidth
    oriY = app.height - 10 - app.rows*cellHeight

    (cRow,cCol) = (app.playerRow,app.playerCol)
    x0 = oriX + cCol*cellWidth
    y0 = oriY + cRow*cellHeight
    x1 = x0 + cellWidth
    y1 = y0 + cellHeight
    canvas.create_rectangle(oriX, oriY, oriX + app.cols*cellWidth, oriY + app.rows*cellHeight,
                            fill = None, outline = 'white')

    canvas.create_rectangle(x0, y0, x1, y1,
                            fill = 'purple', outline = 'purple',width = 5)

    x0 = oriX + app.dropletCol*cellWidth
    y0 = oriY + app.dropletRow*cellHeight
    x1 = x0 + cellWidth
    y1 = y0 + cellHeight
    canvas.create_rectangle(x0, y0, x1, y1,  
                            fill = 'orange', outline = 'orange',width = 5)

# Boids
def initFlock(app,amount):
        for i in range(amount):
            pos = [random.randint(0, app.width*2), random.randint(0, app.height)]
            # gets vector with random direction and magnitude
            vel = multiplyVector(getVector(random.uniform(0, 2*math.pi)), random.uniform(.5, 1))
            acc = [0, 0]
            app.flock.append(Boid(pos, vel, acc))

def handleFlock(app):
        for boid in app.flock: # flock update
            boid.flock(app.flock)
            boid.update(app)

def drawAliens(app, canvas):
    sx = app.scrollX
    sy = app.scrollY
    for boid in app.flock:
        r = 7
        cx, cy = boid.pos
        # vx, vy = self.vel
        # canvas.create_oval(cx-r-sx, cy-r-sy, cx+r-sx, cy+r-sy, fill = 'yellow')
        canvas.create_image(cx-sx, cy - sy,
                        image=ImageTk.PhotoImage(app.image_boid))

def drawTime(app,canvas):
    fontSize = 16
    msg = f"Score: {app.score}"
    canvas.create_text(app.width*0.9, 20, text=msg, 
                        fill='white',font=f'System {fontSize}')

def drawCoord(app,canvas):
    fontSize = 16
    msg = f"PX:{app.playerX},PY:{app.playerY}  Level:{app.level}"
    canvas.create_text(app.width/2, 20, text=msg, fill='white',
                font=f'System {fontSize}')

def drawSpeed(app,canvas):
    totalHeight = app.width // 3
    # vel
    canvas.create_rectangle(10,app.height-30-totalHeight, 20,app.height-10,
                            fill = None, outline = 'white' , width = 1)
    currentVel = readPlayerAbsVel(app)
    speedHeight = totalHeight * currentVel/ app.maxAbsVel
    canvas.create_rectangle(10,app.height-30-speedHeight, 20,app.height-10,
                            fill = 'white', outline = 'white' , width = 1)
    # force
    canvas.create_rectangle(30,app.height-30-totalHeight, 40,app.height-10,
                            fill = None, outline = 'white' , width = 1)
    forceHeight = totalHeight * app.force / app.maxForce
    canvas.create_rectangle(30,app.height-30-forceHeight, 40,app.height-10,
                            fill = 'purple', outline = 'purple' , width = 1)

def drawHealth(app, canvas):
        baseMargin = 10
        baseLength = app.width/4
        baseWidth = 15
        canvas.create_rectangle(baseMargin, baseMargin, baseMargin + baseLength, baseMargin + baseWidth, fill = 'black')
        healthMargin = 0.8
        healthLength = (baseLength - (2 * healthMargin)) * app.health/app.maxHealth
        canvas.create_rectangle(baseMargin + healthMargin, 
                                baseMargin + healthMargin, 
                                baseMargin + healthMargin + healthLength, 
                                baseMargin + baseWidth - healthMargin, 
                                fill = 'white')

def loadSprites(app):
    #sprites https://www.cs.cmu.edu/~112/notes/notes-animations-part4.html#cachingPhotoImages
    spritestrip1 = app.image_player_1
    spritestrip2 = app.image_player_d_1
    spritestrip3 = app.image_player_l_1
    spritestrip4 = app.image_player_r_1

    for i in range(5):
        sprite1 = spritestrip1.crop((0+150*i,0,150+150*i, 380))
        sprite1 = app.scaleImage(sprite1, 0.3)
        app.sprites_1.append(sprite1)

        sprite2 = spritestrip2.crop((0+150*i,0,150+150*i, 380))
        sprite2 = app.scaleImage(sprite2, 0.3)
        app.sprites_2.append(sprite2)

        sprite3 = spritestrip3.crop((0,0+150*i,380,150+150*i))
        sprite3 = app.scaleImage(sprite3, 0.3)
        app.sprites_3.append(sprite3)

        sprite4 = spritestrip4.crop((0,0+150*i,380,150+150*i))
        sprite4 = app.scaleImage(sprite4, 0.3)
        app.sprites_4.append(sprite4)

    app.spriteCounter = 0
    app.cSprites = app.sprites_4
   
def updateRC(app):
    (app.playerRow, app.playerCol) = getCell(app,app.playerX,app.playerY)
    (app.dropletRow, app.dropletCol) = getCell(app,app.dropletX,app.dropletY)

def drawBoundary(app,canvas):
    sx = app.scrollX
    sy = app.scrollY
    nwP = (app.margin-sx,app.margin-sy)
    neP = (app.margin + app.cellWidth*app.cols-sx,app.margin-sy) 
    swP = (app.margin-sx,app.margin + app.cellHeight*app.rows-sy)
    seP = (app.margin + app.cellWidth*app.cols-sx,app.margin + app.cellHeight*app.rows-sy)
    fill = 'gray'
    canvas.create_line(nwP,neP,fill = fill)
    canvas.create_line(nwP,swP,fill = fill)
    canvas.create_line(swP,seP,fill = fill)
    canvas.create_line(neP,seP,fill = fill)

def earnTimeScore(app):
    app.score = app.time // 100 * 100
    if app.score >= app.scoreLine:
        nextLevel(app)

# gameMode_Control
def gameMode_mousePressed(app, event):
    # if not app.isGameOver:
    x = event.x + app.scrollX
    y = event.y + app.scrollY
        #checkForNewWallHit(app)
    putWormhole(app,x,y)
   

def gameMode_keyPressed(app, event):
    if not app.isGameOver:
        if (event.key == "Left"): 
            accPlayer(app,(-app.force,0))
            app.cSprites = app.sprites_3
        elif (event.key == "Right"):
            accPlayer(app,(app.force,0))
            app.cSprites = app.sprites_4
        elif (event.key == "Up"):    
            accPlayer(app,(0,-app.force))
            app.cSprites = app.sprites_1
        elif (event.key == "Down"):
            accPlayer(app,(0,app.force))
            app.cSprites = app.sprites_2
        elif (event.key.lower() == "e" and app.force >= 0.1):
            app.force -= 0.1
            accPlayer(app,app.playerAcc)
        elif (event.key.lower() == "q" and app.force <= app.maxForce-0.1):  
            app.force += 0.1
            accPlayer(app,app.playerAcc)
        elif event.key == "Space":  
            slowDown(app)
        elif (event.key.lower() == "w"):
            flashPlayer(app)
        elif (event.key.lower() == "b"): app.mode = 'splashScreenMode'

def gameMode_timerFired(app):
    if not app.isGameOver:
        movePlayer(app)
        moveDroplet(app)
        handleDroplet(app)
        handleFlock(app)
        updateDropletTrack(app)
        updateRC(app)

        app.time += 1
        earnTimeScore(app)
        app.spriteCounter = (1+app.spriteCounter) % len(app.sprites_1)

def gameMode_redrawAll(app, canvas):
    canvas.create_image(app.width/2, app.height/2,
                        image=ImageTk.PhotoImage(app.image_bg0))
    #drawBaseLine(app,canvas)
    drawWalls(app,canvas)
    drawWormholes(app,canvas)
    drawAliens(app,canvas)
    drawPlayer(app,canvas)
    drawDroplet(app,canvas)
    # draw UI
    drawCoord(app,canvas)
    drawTime(app,canvas)
    drawHealth(app,canvas)
    drawBoundary(app,canvas)
    drawSpeed(app,canvas)
    drawNavMap(app,canvas)

#################################################
# Main App
#################################################
def appStarted(app):
    app.mode = 'backgroundInfo'
    app.label = 'Doomsday Battle!'
    app.size = 0
    app.emptyColor = 'blue'
    (app.rows,app.cols,app.cellWidth,app.cellHeight,app.margin) = gameDimensions()
    app.absWidth = app.cols * app.cellWidth + app.margin*2
    app.absHeight = app.rows * app.cellHeight + app.margin*2

    app.Blocks = [[False]*app.cols for row in range(app.rows)]
    #app.board = [[app.emptyColor]*app.cols for rows in range(app.rows)]
    app.isGameOver = False
    app.time = 0
    app.flashTime = 0
    app.showText = True
    app.score = 0
    app.scoreLine = 500
    app.level = 1

    app.timerDelay = 20

    #image source:https://www.artstation.com/artwork/xzRzxm
    app.image2 = app.loadImage('assets/db_main01.jpg')
    app.image1 = app.scaleImage(app.image2, 0.6)
    #image source:https://www.tor.com/2016/02/08/this-is-how-it-feels-to-read-cixin-lius-the-dark-forest/
    app.image_bg_1 = app.loadImage('assets/db_main02.webp')
    app.image_bg = app.scaleImage(app.image_bg_1, 1.3)
    #image source:https://unblast.com/free-night-sky-star-patterns/
    app.image_bg0_1 = app.loadImage('assets/bg00.jpg')
    app.image_bg0 = app.scaleImage(app.image_bg0_1, 0.5)
    #player image source:https://www.pngitem.com/middle/ToiwmhR_2d-spaceship-pixel-art-hd-png-download/#google_vignette
    app.image_player_1 = app.loadImage('assets/player.png')

    app.image_player_d_1 = app.loadImage('assets/player_d.png')

    app.image_player_l_1 = app.loadImage('assets/player_l.png')

    app.image_player_r_1 = app.loadImage('assets/player_r.png')

    #image source:https://www.pngfind.com/mpng/ibwxwbR_water-droplet-test-pixel-art-dhmis-hd-png/
    app.image_droplet_1 = app.loadImage('assets/droplet.png')
    app.image_droplet = app.scaleImage(app.image_droplet_1, 0.1)
    #wormhole image source:http://pixelartmaker.com/art/17ec2e360e8753e
    app.image_wormhole_1 = app.loadImage('assets/wormhole.png')
    app.image_wormhole = app.scaleImage(app.image_wormhole_1, 0.5)
    #boids image source:https://www.freepik.com/free-photos-vectors/eye-pixel-art
    app.image_boid_1 = app.loadImage('assets/boid.png')
    app.image_boid = app.scaleImage(app.image_boid_1, 0.3)

    # scroll
    app.scrollX = 0 
    app.scrollY = 0 
    app.scrollMargin = 150

    # player
    app.playerWidth = 30
    app.playerHeight = 30
    app.force = 0.1
    app.maxAbsVel = 15
    app.maxForce = 0.8
    #app.playerSpeed = 3 #positive integer
    app.playerX = app.scrollMargin
    app.playerY = app.scrollMargin

    (app.playerRow, app.playerCol) = getCell(app,app.playerX,app.playerY)
    app.playerAcc = (0.2,0)
    app.playerVel = (1,0)
    app.playerDir = (1,0)
    app.maxHealth = 1000
    app.health = app.maxHealth
    
    app.dropletX  = app.width - app.margin
    app.dropletY  = app.height - app.margin
    (app.dropletRow,app.dropletCol) = getCell(app,app.dropletX,app.dropletY)
    app.dropletTrack = []
    app.targetX = app.playerX
    app.targetY = app.playerY
    app.pathVal = 0
    app.path = []
    app.dropletSpeed = 4

    app.walls = set()
    app.wallWidth = 50
    app.wallHeight = 300
    app.wallSpacing = 200
    app.currentWallHit = -1 # start out not hitting a wall
    generateWalls(app,40)

    app.wormholes = set()
    generateWormhole(app,3)

    app.flock = []
    initFlock(app,40)

    app.sprites_1 = [ ]
    app.sprites_2 = [ ]
    app.sprites_3 = [ ]
    app.sprites_4 = [ ]
    loadSprites(app)

def playGame():   
    # (rows, cols, cellWidth, cellHeight, margin) = gameDimensions()
    # width = roundHalfUp(cellWidth*cols + margin*2)
    # height = roundHalfUp(cellHeight*rows + margin*2)
    width = 1000
    height = 600
    runApp(width=width, height=height)

#################################################
# Helper functions
#################################################

def almostEqual(d1, d2, epsilon=10**-7):
    # note: use math.isclose() outside 15-112 with Python version 3.5 or later
    return (abs(d2 - d1) < epsilon)

import decimal
def roundHalfUp(d):
    # Round to nearest with ties going away from zero.
    rounding = decimal.ROUND_HALF_UP
    # See other rounding options here:
    # https://docs.python.org/3/library/decimal.html#rounding-modes
    return int(decimal.Decimal(d).to_integral_value(rounding=rounding))

def make2dList(rows, cols):
    return [ ([0] * cols) for row in range(rows) ]

def distance(x1, y1, x2, y2):
    return ((x1 - x2)**2 + (y1 - y2)**2)**0.5 
    
#################################################
# main
#################################################

def main():
    playGame()

if __name__ == '__main__':
    main()
