from cmu_112_graphics import *
from doomsdayBattle import *

def flashText(app):
    app.flashTime += 1
    if app.flashTime >= 10:
        app.showText = not app.showText
        app.flashTime = 0
#################################################
# Background Information
#################################################

def backgroundInfo_redrawAll(app, canvas):
    canvas.create_image(app.width//2, app.height//2,
                        image=ImageTk.PhotoImage(app.image_bg))
    fontSize = 26 
    canvas.create_text(app.width/2, 30, 
                        text='[ Background ]', 
                       font=f'System {20} bold', fill='gray')
    canvas.create_text(app.width/2, 100, 
                        text='In Year 205, Crisis Era',
                       font=f'System {fontSize} bold', fill='white')

    canvas.create_text(app.width/2, app.height - 100, text='''\
One Trisolaran Droplet arrives in the solar system.
Humans sent their entire Solar Fleet Joint Conference Combined Fleet of 2000 'Star' spacecraft\nto achieve this 'First Contact'
''',
                       font= f'System {16} bold', fill='white')
    if app.showText:
        canvas.create_text(app.width/2, app.height - 30, 
                            text='Press any key',
                        font=f'System {20} bold', fill='purple')

def backgroundInfo_keyPressed(app, event):
    app.mode = 'splashScreenMode'

def backgroundInfo_timerFired(app):
    flashText(app)


from cmu_112_graphics import *

##########################################
# Splash Screen Mode
##########################################
def splashScreenMode_redrawAll(app,canvas):
    canvas.create_image(app.width/2, app.height/2,
                        image=ImageTk.PhotoImage(app.image1))
    text = f'''\
[The Doomsday Battle]

Press [0] to Background
Press other keys to START


RUN !!!

press arrow keys to change direction
press [w] to flash
press [space] to slow down
press [q] and [e] to control power system
'''
    textSize = min(app.width,app.height) // 30
    canvas.create_text(app.width/2, app.height/2, text=text, fill='white',
                       font=f'System {textSize} bold')

def splashScreenMode_keyPressed(app,event):
    
        
    if event.key == '0':
        app.mode = 'backgroundInfo'
    else:
        app.mode = 'gameMode'

#################################################
# EndScreen
#################################################

def endScreenMode_redrawAll(app, canvas):
    canvas.create_image(app.width/2, app.height/2,
                        image=ImageTk.PhotoImage(app.image1))
    fontSize = 30
    canvas.create_text(app.width/2, 50, 
                        text='[ Game Over ]', 
                       font=f'System {20} bold', fill='purple')
    canvas.create_text(app.width/2, app.height // 2, 
                        text=f'Score:{app.score}',
                       font=f'System {fontSize} bold', fill='white')

    canvas.create_text(app.width/2, app.height // 2 + 50, text='''\
'Weakness and ignorance are not barriers to survival, but arrogance is.'
''',
                       font= f'System {16} bold', fill='white')
    if app.showText:
        canvas.create_text(app.width/2, app.height - 50, 
                            text='Press [Space] to Restart',
                        font=f'System {20} bold', fill='purple')

def endScreenMode_keyPressed(app, event):
    if event.key == 'Space':
        appStarted(app)

def endScreenMode_timerFired(app):
    flashText(app)