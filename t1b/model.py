from OpenGL.GL import *
from random import randint

from libs import basic_shapes as bs
from libs import transformations as tr
from libs import easy_shaders as es
from libs import scene_graph as sg

class Background:
    def __init__(self):
        ## Fondo
        gpuBackground= es.toGPUShape(bs.createTextureQuad("images/background1.jpg"), GL_REPEAT, GL_NEAREST)

        background = sg.SceneGraphNode("background")
        background.transform = tr.uniformScale(2)
        background.childs = [gpuBackground]

        ##Fondos trasladados para realizar infinite scrolling background
        translatedBackground1 = sg.SceneGraphNode("translatedBackground1")
        translatedBackground1.childs = [background]

        translatedBackground2 = sg.SceneGraphNode("translatedBackground2")
        translatedBackground2.childs = [background]

        scrollingBackground = sg.SceneGraphNode("scrollingBackground")
        scrollingBackground.childs = [translatedBackground1, translatedBackground2]

        self.node = scrollingBackground
        self.background1 = translatedBackground1
        self.background2 = translatedBackground2
        self.pos = 2
        self.speed = 0.0005

    def update(self):
        if self.pos< 0:
            self.pos = 2
        self.background1.transform = tr.translate(0, 2 - self.pos ,0)
        self.background2.transform = tr.translate(0, -self.pos,0)
        self.node.childs = [self.background1,self.background2]
        self.pos -= self.speed

class Ship:
    def __init__(self):
        gpuShip= es.toGPUShape(bs.createTextureQuad("images/ship.png"), GL_REPEAT, GL_NEAREST)
        ##Nave jugador
        ship = sg.SceneGraphNode("ship")
        ship.transform = tr.uniformScale(0.1)
        ship.childs = [gpuShip]
        ##Nave jugador trasladada
        translatedShip = sg.SceneGraphNode("translatedShip")
        translatedShip.transform = tr.translate(0, -0.9,0)
        translatedShip.childs = [ship]

        self.node = translatedShip
        self.x = 0
        self.y = -0.9

    def update(self,dx,dy):
        self.node.transform = tr.translate(dx, -0.9 + dy,0)
        self.x = dx
        self.y = -0.9 + dy

class Enemys:
    def __init__(self):
        gpuEnemy = es.toGPUShape(bs.createTextureQuad("images/enemy.jpg"), GL_REPEAT, GL_NEAREST)

        enemy = sg.SceneGraphNode("enemy")
        enemy.transform = tr.uniformScale(0.1)
        enemy.childs = [gpuEnemy]

        self.enemy = enemy
        self.nodes = []
        self.x = []
        self.y = []
        self.xspeed =  0.01
        self.yspeed =  0.1

    def createEnemy(self,x):
        translatedEnemy = sg.SceneGraphNode("translatedEnemy")
        translatedEnemy.transform = tr.translate(x,0.9,0)
        translatedEnemy.childs = [self.enemy]

        self.nodes += [translatedEnemy]
        self.x += [x]
        self.y += [0.9]

    def removeEnemys(self,l):
        nodes = []
        x = []
        y = []

        for i in range(len(self.nodes)):
            if (i in l):
                pass
            else:
                nodes += [self.nodes[i]]
                x += [self.x[i]]
                y += [self.y[i]]

        self.nodes = nodes
        self.x = x
        self.y = y

    def update(self):
        for i in range(len(self.nodes)):
            self.x[i] += self.xspeed
            if self.x[i] > 0.9:
                self.x[i] = -0.9
                self.y[i] -= self.yspeed
            self.nodes[i].transform = tr.translate(self.x[i],self.y[i],0)

class Shot:
    def __init__(self):
        gpuShot = es.toGPUShape(bs.createTextureQuad("images/pelota.png"), GL_REPEAT, GL_NEAREST)
        shot = sg.SceneGraphNode("shot")
        shot.transform = tr.uniformScale(0.1)
        shot.childs = [gpuShot]
        
        self.shot = shot
        self.nodes = []
        self.x = []
        self.y = []
        self.speed = 0.05
        self.count = 0

    def createShot(self,ship):
        if self.count > 20:
            translatedShot= sg.SceneGraphNode("translatedShot")
            translatedShot.transform = tr.translate(ship.x,ship.y + 0.1,0)
            translatedShot.childs = [self.shot]
            self.nodes += [translatedShot]
            self.x += [ship.x]
            self.y += [ship.y]
            self.count = 0

    def removeShot(self,l):
        nodes = []
        x = []
        y = []

        for i in range(len(self.nodes)):
            if i in l:
                pass
            else:
                nodes += [self.nodes[i]]
                x += [self.x[i]]
                y += [self.y[i]]
        self.nodes = nodes
        self.x = x
        self.y = y

    def update(self):
        nodes = []
        x = []
        y = []
        for i in range(len(self.nodes)):
            self.y[i] += self.speed
            if self.y[i] > 1:
                pass
            else:
                self.nodes[i].transform = tr.translate(self.x[i], self.y[i],0)
                nodes += [self.nodes[i]]
                x += [self.x[i]]
                y += [self.y[i]]
        self.nodes = nodes
        self.x = x
        self.y = y
        self.count += 1

class Model:
    def __init__(self,n):
        background = Background()
        ship = Ship()
        enemys = Enemys()
        shot = Shot()

        enemys.createEnemy(0)

        spaceInvaders = sg.SceneGraphNode("spaceInvader")
        spaceInvaders.childs = [background.node, ship.node]
        spaceInvaders.childs += enemys.nodes

        self.scene = spaceInvaders
        self.background = background
        self.ship = ship
        self.enemys = enemys
        self.shot = shot 
        self.count = 0
        self.n = n-1
        self.enemyslive = n

    def addEnemy(self):
        self.count += 1
        if self.count == 10:
            self.count = 0
            a = randint(0,10)

            if a == 0:
                a = randint(0,9)
                a /= 10
                self.enemys.createEnemy(a)
                self.n -= 1

    def eliminateEnemys(self,l):
        self.enemys.removeEnemys(l)

    def eliminateShot(self,l):
        self.shot.removeShot(l)

    def addShot(self):
        self.shot.createShot(self.ship)

    def crashShotEnemy(self):
        le = []
        ls = []

        for i in range(len(self.shot.y)):
            for j in range(len(self.enemys.y)):
                if self.shot.y[i] > self.enemys.y[j] -0.01 and self.shot.y[i] < self.enemys.y[j] + 0.01:
                    if self.shot.x[i] > self.enemys.x[j] - 0.06 and self.shot.x[i] < self.enemys.x[j] + 0.06:
                        le += [j]
                        ls += [i]
                        self.enemyslive -=1
        self.eliminateEnemys(le)
        self.eliminateShot(ls)


    def update(self,dx,dy,shot):
        if shot == True:
            self.addShot()

        if self.n > 0:
            self.addEnemy()

        self.background.update()
        self.ship.update(dx,dy)
        self.enemys.update()
        self.shot.update()
        self.crashShotEnemy()

        self.scene.childs = [self.background.node, self.ship.node]
        self.scene.childs += self.enemys.nodes
        self.scene.childs += self.shot.nodes


