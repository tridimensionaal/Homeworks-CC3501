from OpenGL.GL import *

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

    def update(self):
        if self.pos< 0:
            self.pos = 2
        self.background1.transform = tr.translate(0, 2 - self.pos ,0)
        self.background2.transform = tr.translate(0, -self.pos,0)
        self.node.childs = [self.background1,self.background2]
        self.pos -= 0.001

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

    def createEnemy(self,x):
        translatedEnemy = sg.SceneGraphNode("translatedEnemy")
        translatedEnemy.transform = tr.translate(x,0.9,0)
        translatedEnemy.childs = [self.enemy]

        self.nodes += [translatedEnemy]
        self.x += [x]
        self.y += [0.9]

    def update(self):
        for i in range(len(self.nodes)):
            self.x[i] += 0.01
            if self.x[i] > 0.9:
                self.x[i] = -0.9
                self.y[i] -= 0.1
            self.nodes[i].transform = tr.translate(self.x[i],self.y[i],0)

class Model:
    def __init__(self):
        background = Background()
        ship = Ship()
        enemys = Enemys()

        enemys.createEnemy(0)

        spaceInvaders = sg.SceneGraphNode("spaceInvader")
        spaceInvaders.childs = [background.node, ship.node]
        spaceInvaders.childs += enemys.nodes

        self.scene = spaceInvaders
        self.background = background
        self.ship = ship
        self.enemys = enemys
        
    def update(self,dx,dy):
        self.background.update()
        self.ship.update(dx,dy)
        self.enemys.update()

        self.scene.childs = [self.background.node, self.ship.node]
        self.scene.childs += self.enemys.nodes


