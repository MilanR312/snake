import keyboard as kb
import numpy as np
import cv2 as cv
import time

width = height = 50

field = np.zeros((width, height, 3), dtype='uint8')

velocity = [0,0]
base_speed = 1

fps = 15

class player:
    def __init__(self) -> None:
        self.x = 25
        self.y = 25
        self.vx = 0
        self.vy = 0
        self.size = 0
        self.c = 0
        field[self.x][self.y] = (255, 0, 0)
    def setVY(self, val) -> None:
        self.vy = val
    def setVX(self, val) -> None:
        self.vx = val
    def initmove(self):
        field[self.y][self.x] = (0, 0, 0)
    def update(self):
        self.x += self.vx
        self.y += self.vy
        if field[self.y][self.x][2] == 255:
            self.size += 1
            print(self.size)
        field[self.y][self.x] = (255, 0, 0)
    def getVel(self) -> tuple:
        return (self.vx, self.vy)
    def getPos(self) -> tuple:
        return (self.x, self.y)

P1 = player()

class body:
    def __init__(self, x, y) -> None:
        (self.x, self.y) = x,y
        field[self.y][self.x] = (0, 255, 0)
        self.live = P1.size
    def age(self):
        self.live -= 1
        if self.live < 0:
            field[self.y][self.x] = (0, 0, 0)
            return 0
        return 1

alivebodies = []

def GenerateApple():
    x,y = np.random.randint(0, width), np.random.randint(0, height)
    print(x,y)
    z = 0
    for i in range(3):
        z += field[x][y][i]
        if z == 0:
            field[x][y] = ( 0, 0, 255)

def key():
    if kb.is_pressed('right'):
        P1.setVX(base_speed)
        P1.setVY(0)
    if kb.is_pressed('left'):
        P1.setVX(-base_speed)
        P1.setVY(0)
    if kb.is_pressed('up'):
        P1.setVY(-base_speed)
        P1.setVX(0)
    if kb.is_pressed('down'):
        P1.setVY(base_speed)
        P1.setVX(0)

lentem = 0
def Apples():
    global lentem
    if lentem == P1.size:
        GenerateApple()
        lentem += 1
BodyParts  = []
def GenBodyPart():
    BodyParts.append(body(P1.getPos()[0], P1.getPos()[1]))
    for i in BodyParts:
        if i.age() == 0:
            BodyParts.remove(i)
    print(len(BodyParts))

def fpslimited():
    P1.initmove()
    GenBodyPart()
    P1.update()
    Apples()
    out = cv.resize(field, (1000, 1000), interpolation=cv.INTER_AREA)
    cv.imshow("test", out)
    cv.waitKey(1)

def nonfpslimited():
    key()

toRun = 0.0
while True:
    nonfpslimited()

    if abs(toRun - time.time()) > 1/fps:
        toRun = time.time() + 1/fps
        fpslimited()