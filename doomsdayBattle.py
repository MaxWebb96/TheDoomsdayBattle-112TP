#################################################
# The Doomsday Battle(112 Term Project)
# Verson: 0.1
# Last Updated: 19 Nov
# Autor: Zain Hao (andrew id: xingh)
#################################################

import math, copy, random
import class_DB
from cmu_112_graphics import *

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

#################################################
# mainMenu
#################################################
def mainMenu_redrawAll(app,canvas):
    canvas.create_image(app.width/2, app.height/2,
                        image=ImageTk.PhotoImage(app.image1))
    text = f'''\
[The Doomsday Battle]

Press the number key for the Next:
0. Background
1. Play
2. Options
'''
    textSize = min(app.width,app.height) // 30
    canvas.create_text(app.width/2, app.height/2, text=text, fill='white',
                       font=f'Arial {textSize} bold')

def mainMenu_keyPressed(app,event):
    if event.key == '1':
        app.mode = 'gameMode'
    if event.key == '0':
        app.mode = 'backgroundInfo'

#################################################
# Game Mode
#################################################
def gameDimensions():
    rows = 15
    cols = 15
    tileHeight = 30
    tileWidth = 30
    margin = 40
    return (rows, cols, tileWidth,tileHeight, margin)

def cartToIso(X,Y):
    isoX = X-Y
    isoY = (X+Y)/2
    return (isoX,isoY)

def isoToCart(isoX,isoY):
    X = ((2 * isoY + isoX) / 2)
    Y = ((2 * isoY - isoX) / 2)
    return (X, Y)

def drawMapCell(app,canvas,X,Y,size,color):
    canvas.create_rectangle(X,Y,X+size,
    Y+size,fill=color,outline='black')

def drawNavMap(app,canvas):
    canvas.create_rectangle(app.navMapX-app.navMapSize/2,
    app.navMapY-app.navMapSize/2,
    app.navMapX+app.navMapSize/2,
    app.navMapY+app.navMapSize/2,
    fill = app.color, outline = 'black', width = 3)

    originX = app.navMapX - app.navMapSize/2
    originY = app.navMapY - app.navMapSize/2
    for i in range(app.rows):
        for j in range(app.cols):
            x = originX + j*app.navMapCellSize
            y = originY + i*app.navMapCellSize
            #drawMapCell(app,canvas,x,y,app.cellSize,app.board[i][j])
            drawMapCell(app,canvas,x,y,app.navMapCellSize,'blue')

def drawIsoCell(app,canvas,pointList,color):
    canvas.create_polygon(cartToIso(pointList[0][0],pointList[0][1]),
    cartToIso(pointList[1][0],pointList[1][1]),
    cartToIso(pointList[2][0],pointList[2][1]),
    cartToIso(pointList[3][0],pointList[3][1]),
    outline = 'black', width = 2,
    fill = color
    )
    
def drawIsoBoard(app,canvas):
    originX = app.width * 0.32 #To SE
    originY = -app.height * 0.25 #To SW
    tileWidth = app.tileWidth
    tileHeight = app.tileHeight
    for row in range(app.rows):
        for col in range(app.cols):
            pointList = [[0]*2 for row in range(4)]
            pointList[0][0] = originX + tileWidth*row
            pointList[0][1] = originY + tileHeight*col
            pointList[1][0] = originX + (tileWidth*(row + 1))
            pointList[1][1] = originY + (tileHeight*col)
            pointList[2][0] = originX + (tileWidth*(row + 1))
            pointList[2][1] = originY + (tileHeight*(col + 1))
            pointList[3][0] = originX + (tileWidth*row)
            pointList[3][1] = originY + (tileHeight*(col + 1))
            if app.cellMap_My[row][col] == 1:
                drawIsoCell(app,canvas,pointList,'red')
            else:
                drawIsoCell(app,canvas,pointList,'gray')

def cellMap_My_reset(app):
    app.cellMap_My = [[0]*app.cols for row in range(app.rows)]
    app.cellMap_My[app.currentX][app.currentY] = 1

def moveMy(app,moveX,moveY):
    if app.currentX + moveX < app.rows and app.currentX + moveX >= 0:
        app.currentX += moveX
    if app.currentY + moveY < app.cols and app.currentY + moveY >= 0:
        app.currentY += moveY
    cellMap_My_reset(app)

def populateSpacecraft(app,canvas):
    pass

def cellMap_Droplet(app,canvas):
    pass
    
def drawTime(app,canvas):
    canvas.create_text(app.width/2, app.margin/2, fill= 'black',
                        text= f'Survival Time:{roundHalfUp(app.time)}', 
                        font=f'Arial {app.margin//2} bold')

def drawNavM_Text(app,canvas):
    canvas.create_text(app.navMapX, app.navMapY - app.navMapSize/2-10,
                        fill= 'blue',
                        text= f'Navigation Map', 
                        font=f'Arial {app.margin//3} bold')

    canvas.create_text(app.navMapX, app.navMapY + app.navMapSize/2+10,
                        fill= 'blue',
                        text= f'Current Coordinate: {app.currentX},{app.currentY}', 
                        font=f'Arial {app.margin//3} bold')
    
    canvas.create_text(app.navMapSize/2 + app.margin*3, app.navMapY,
                        fill= 'black',
                        text= 'Press H to go homepage', 
                        font=f'Arial {app.margin//2} bold')

def gameMode_redrawAll(app,canvas):
    drawIsoBoard(app,canvas)
    drawNavMap(app,canvas)
    drawTime(app,canvas)
    drawNavM_Text(app,canvas)

def gameMode_keyPressed(app, event):
    if event.key.lower() == 'h':
        app.mode = 'mainMenu' 
        app.time = 0
    elif event.key == 'Down': moveMy(app,1,0)
    elif event.key == 'Left': moveMy(app,0,-1)
    elif event.key == 'Right': moveMy(app,0,1)
    elif event.key == 'Up': moveMy(app,-1,0)
    # if event.key == 'Space': rotateFallingPiece(app)
    
    # elif event.key =='r': appStarted(app)

def gameMode_timerFired(app):
    if not app.isGameOver:
    #moveDroplet()
        app.time += 0.2

#################################################
# Background Information
#################################################

def backgroundInfo_redrawAll(app, canvas):
    canvas.create_image(app.width//2, app.height//2,
                        image=ImageTk.PhotoImage(app.image_bg))
    fontSize = 26 
    canvas.create_text(app.width/2, 30, 
                        text='Background', 
                       font=f'Arial {20} bold', fill='white')
    canvas.create_text(app.width/2, 250, 
                        text='In Year 205, Crisis Era',
                       font=f'Arial {fontSize} bold', fill='white')
    canvas.create_text(app.width/2, 350, text='''\
One Trisolaran Droplet arrives in the solar system.
Humans sent their entire Solar Fleet Joint Conference Combined Fleet of 2000 'Star' spacecraft\nto achieve this 'First Contact'
''',
                       font= f'Arial {20} bold', fill='white')

    canvas.create_text(app.width/2, app.height - 30, 
                        text='Press any key to go back',
                       font=f'Arial {20} bold', fill='white')

def backgroundInfo_keyPressed(app, event):
    app.mode = 'mainMenu'

#################################################
# Main App
#################################################
def appStarted(app):
    app.mode = 'mainMenu'
    app.label = 'Doomsday Battle!'
    app.color = 'orange'
    app.size = 0
    app.emptyColor = 'blue'
    (app.rows,app.cols,app.tileWidth,app.tileHeight,app.margin) = gameDimensions()

    #app.board = [[app.emptyColor]*app.cols for rows in range(app.rows)]
    app.isGameOver = False
    app.time = 0
    app.score = 0
    app.timerDelay = 200

    #image source:https://www.artstation.com/artwork/xzRzxm
    app.image2 = app.loadImage('assets/db_main01.jpg')
    app.image1 = app.scaleImage(app.image2, 0.6)
    #image source:https://www.tor.com/2016/02/08/this-is-how-it-feels-to-read-cixin-lius-the-dark-forest/
    app.image_bg2 = app.loadImage('assets/db_main02.webp')
    app.image_bg = app.scaleImage(app.image_bg2, 1.3)

    app.navMapCellSize = 10
    app.navMapSize = min(app.width,app.height)//4
    app.navMapX = app.width - app.navMapSize/2 - app.margin
    app.navMapY = app.height - app.navMapSize/2 - app.margin

    app.cellMap_My = [[0]*app.cols for row in range(app.rows)]
    app.currentX = app.rows//2
    app.currentY = app.cols//2
    cellMap_My_reset(app)

def playGame():   
    (rows, cols, tileWidth,tileHeight, margin) = gameDimensions()
    width = roundHalfUp(tileWidth*rows*2 + margin*2)
    height = roundHalfUp(tileHeight*cols*1.2 + margin*2)
    runApp(width=width, height=height)

#################################################
# main
#################################################

def main():
    playGame()

if __name__ == '__main__':
    main()
