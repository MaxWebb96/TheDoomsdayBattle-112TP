#################################################
# The Doomsday Battle(112 Term Project)
# Verson: 0.1
# Last Updated: 19 Nov
# Autor: Zain Hao (andrew id: xingh)
#################################################

class Spacecraft:
    def __init__(self,mass,speed):
        self.speed = speed
        self.mass = mass
        self.direction = speed

    def explosion(self):
        pass

    def changeDirection(self):
        pass


class Droplet:
    def __init__(self,mass,speed):
        self.mass = mass
        self.speed = speed

    def chasing(self):
        pass

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