from OpenGL.GL import *
from random import randint

from libs import basic_shapes as bs
from libs import transformations as tr
from libs import easy_shaders as es
from libs import scene_graph as sg

#Clase que se encaga de cargar la textura del fondo e implementar la lógica necesaria para realizar un infinte scrolling background.
class Background:
    def __init__(self):
        ## Se carga la textura del fondo
        gpuBackground= es.toGPUShape(bs.createTextureQuad("images/background1.jpg"), GL_REPEAT, GL_NEAREST)
        #Se crea el nodo asociado al fondo
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

        #Atributos de la clase
        self.node = scrollingBackground
        self.background1 = translatedBackground1
        self.background2 = translatedBackground2
        self.pos = 2
        #Velocidad a la cual se mueve el fondo 
        self.speed = 0.0005

    #Función que actualiza el fondo
    def update(self):
        if self.pos< 0:
            self.pos = 2
        #Se mueve el fondo
        self.background1.transform = tr.translate(0, 2 - self.pos ,0)
        self.background2.transform = tr.translate(0, -self.pos,0)
        self.node.childs = [self.background1,self.background2]
        self.pos -= self.speed

#Clase que se encaga de cargar las texturas de la nave del jugador e implementar la lógica necesaria para su funcionamiento
class Ship:
    def __init__(self):
        #Se cargan las dos texturas de la nave. Se quiere tener dos texturas ya que, al disparar la nave, ésta va a cambiar de forma.
        gpuShip1= es.toGPUShape(bs.createTextureQuad("images/ship1.png"), GL_REPEAT, GL_NEAREST)
        gpuShip2= es.toGPUShape(bs.createTextureQuad("images/ship2.png"), GL_REPEAT, GL_NEAREST)
        ##Nave jugador forma normal
        ship1 = sg.SceneGraphNode("ship")
        ship1.transform = tr.uniformScale(0.1)
        ship1.childs = [gpuShip1]

        #Nave jugador forma disparo
        ship2 = sg.SceneGraphNode("ship")
        ship2.transform = tr.uniformScale(0.1)
        ship2.childs = [gpuShip2]
 
        ##Nave jugador normal trasladada
        translatedShip = sg.SceneGraphNode("translatedShip")
        translatedShip.transform = tr.translate(0, -0.9,0)
        translatedShip.childs = [ship1]

        #Atributos de la clase
        self.ship1 = ship1
        self.ship2 = ship2
        self.node = translatedShip
        self.x = 0
        self.y = -0.9
        #Contador para que, cuando se cambie la nave de forma normal a forma disparo, la nave mantenga un pequeño tiempo la forma disparo
        self.count = 0

    #Función que actualiza la nave dados los parametros entregados por el usuario
    def update(self,dx,dy,shot):
        #Si se disparó, la nave cambia de forma a forma disparo
        if shot == True:
            self.count = 1
            self.node.childs = [self.ship2]

        #Si la nave se encuentra en forma disparo, entonces self.count > 0
        if self.count > 0:

            #Si ha pasado un pequeño tiempo, la nave vuelve a forma normal
            if self.count == 20:
                self.node.childs = [self.ship1]
                self.count = 0
            self.count += 1

        #Se actualiza la posición de la nave
        self.node.transform = tr.translate(dx, -0.9 + dy,0)
        self.x = dx
        self.y = -0.9 + dy

#Clase que se encaga de cargar las texturas de las naves enemigas e implementar la lógica necesaria para su funcionamiento
class Enemys:
    def __init__(self):

        #Se cargan las dos texturas de la nave. Se quiere tener dos texturas ya que, las naves enemigas van cambiando de forma mientras se mueven.
        gpuEnemy1 = es.toGPUShape(bs.createTextureQuad("images/enemy1.png"), GL_REPEAT, GL_NEAREST)
        gpuEnemy2 = es.toGPUShape(bs.createTextureQuad("images/enemy2.png"), GL_REPEAT, GL_NEAREST)

        #Nave enemiga 1
        enemy1 = sg.SceneGraphNode("enemy")
        enemy1.transform = tr.uniformScale(0.1)
        enemy1.childs = [gpuEnemy1]

        #Nave enemiga 2
        enemy2 = sg.SceneGraphNode("enemy")
        enemy2.transform = tr.uniformScale(0.1)
        enemy2.childs = [gpuEnemy2]

        #Atributos de la clase
        self.enemy1 = enemy1
        self.enemy2 = enemy2
        self.nodes = []
        self.x = []
        self.y = []
        self.xspeed =  0.01
        self.yspeed =  0.1
        #Contador para que, cada cierto tiempo, las naves enemigas cambien su forma
        self.count = 0

    #Función que, dada una posición x, crea una nave enemiga en la posición (x,0.9)
    def createEnemy(self,x):
        translatedEnemy = sg.SceneGraphNode("translatedEnemy")
        translatedEnemy.transform = tr.translate(x,0.9,0)

        #Dependiendo del valor del contador, se define que textura usar.
        if self.count < 20:
            translatedEnemy.childs = [self.enemy1]
        else:
            translatedEnemy.childs = [self.enemy2]

        self.nodes += [translatedEnemy]
        self.x += [x]
        self.y += [0.9]

    #Función que, dado un índice, elimina la nave asociada a ese índice
    def removeEnemys(self,i):
        self.nodes.pop(i)
        self.x.pop(i)
        self.y.pop(i)

    #Función que actualiza las naves enemigas
    def update(self):
        #Se actualiza las posiciones de las naves, dependiendo del contador, se cambia la textura asociada a las naves o se mantiene.

        if self.count == 20:
            #Las naves se cambian a la segunda textura
            for i in range(len(self.nodes)):
                self.x[i] += self.xspeed
                if self.x[i] > 0.9:
                    self.x[i] = -0.9
                    self.y[i] -= self.yspeed
                self.nodes[i].childs = [self.enemy2]
                self.nodes[i].transform = tr.translate(self.x[i],self.y[i],0)

        elif self.count == 40:
            #Las naves se cambian a la primera textura
            for i in range(len(self.nodes)):
                self.x[i] += self.xspeed
                if self.x[i] > 0.9:
                    self.x[i] = -0.9
                    self.y[i] -= self.yspeed
                self.nodes[i].childs = [self.enemy1]
                self.nodes[i].transform = tr.translate(self.x[i],self.y[i],0)
        else:
            #Las naves mantienen su textura
            for i in range(len(self.nodes)):
                self.x[i] += self.xspeed
                if self.x[i] > 0.9:
                    self.x[i] = -0.9
                    self.y[i] -= self.yspeed
                self.nodes[i].transform = tr.translate(self.x[i],self.y[i],0)
 

        #Se actualiza el contador
        if self.count == 40:
            self.count = 0
        self.count += 1

#Clase que se encaga de cargar la textura del disparo de la nave del jugador e implementar la lógica necesaria para su funcionamiento
class Shot:
    def __init__(self):
        #Se carga la textura
        gpuShot = es.toGPUShape(bs.createTextureQuad("images/shot.png"), GL_REPEAT, GL_NEAREST)
        shot = sg.SceneGraphNode("shot")
        shot.transform = tr.uniformScale(0.1)
        shot.childs = [gpuShot]
        
        #Atributo de la clase
        self.shot = shot
        self.nodes = []
        self.x = []
        self.y = []
        self.speed = 0.05
        #Se quiere que la nave no dispare constatemente, para eso, se define un contador que regular la cantidad de disparos 
        self.count = 0

    #Función que, dada la nave del jugador, crea un disparo
    def createShot(self,ship):
        #Si el contador es mayor a 20, la nave puede disparar
        if self.count > 20:
            #Se agrega una nueva bala dependiendo de la posicón de la nave del jugador.
            translatedShot= sg.SceneGraphNode("translatedShot")
            translatedShot.transform = tr.translate(ship.x,ship.y + 0.1,0)
            translatedShot.childs = [self.shot]
            self.nodes += [translatedShot]
            self.x += [ship.x]
            self.y += [ship.y]
            self.count = 0

    #Función que, dado un índice, se elimina el disparo asociado al índice
    def removeShot(self,i):
        self.nodes.pop(i)
        self.x.pop(i)
        self.y.pop(i)

    #Función que actualiza los disparos 
    def update(self):
        nodes = []
        x = []
        y = []
        for i in range(len(self.nodes)):
            self.y[i] += self.speed

            #Si una bala está fuera de la pantalla, se elimina
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

        if self.count > 21:
            self.count = 21

#Clase que se encaga de cargar la textura del disparo de las naves enemigas e implementar la lógica necesaria para su funcionamiento
class EnemyShot:
    def __init__(self):
        #Se carga la textura
        gpuEnemyShot = es.toGPUShape(bs.createTextureQuad("images/enemyshot.png"), GL_REPEAT, GL_NEAREST)
        enemyshot = sg.SceneGraphNode("enemyshot")
        enemyshot.transform = tr.uniformScale(0.1)
        enemyshot.childs = [gpuEnemyShot]

        #Atributos de la clase
        self.enemyshot = enemyshot
        self.nodes = []
        self.x = []
        self.y = []
        self.speed =  -0.05
        #Se quiere que las naves enemigas no disparen constatemente, para eso, se define un contador que regula la cantidad de disparos
        self.count = 0

    #Función que, dado los enemigos, crea un disparo por cada enemigo que se encuentra en la posición más inferior de la pantalla para todo x.
    def createEnemyShot(self,enemys):
        #Se dispara cada cierto tiempo
        if self.count == 100:
            self.count = 0
            x = []
            for i in range(len(enemys.nodes)):
                if int(10*(enemys.x[i]+0.02)) in x:
                    pass
                else:
                    translatedEnemyShot= sg.SceneGraphNode("translatedEnemyShot")
                    translatedEnemyShot.transform = tr.translate(enemys.x[i],enemys.y[i]-0.1,0)
                    translatedEnemyShot.childs = [self.enemyshot]
                    self.nodes += [translatedEnemyShot]
                    self.x += [enemys.x[i]]
                    self.y += [enemys.y[i] - 0.1 ]
                    x += [int(10*enemys.x[i])]

    #Función que, dado un índice, remueve la bala enemiga asociada al índice
    def removeEnemyShot(self,i):
        self.nodes.pop(i)
        self.x.pop(i)
        self.y.pop(i)

    #Función que actualiza los disparos 
    def update(self):
        nodes = []
        x = []
        y = []
        for i in range(len(self.nodes)):
            self.y[i] += self.speed
            #Si el disparo sale de la pantalla, entonces se elimina
            if self.y[i] < -1:
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

#Clase que se encargar de cargar todos los elementos del juego y de implementar las lógicas del juego
class Model:
    def __init__(self,n):
        #Se cargan los diversos elementos del juego
        background = Background()
        ship = Ship()
        enemys = Enemys()
        shot = Shot()
        enemyshot = EnemyShot()

        #Se crea un enemigo inicial
        enemys.createEnemy(0)

        #Nodo que representa la escena
        spaceInvaders = sg.SceneGraphNode("spaceInvader")
        spaceInvaders.childs = [background.node, ship.node]
        spaceInvaders.childs += enemys.nodes

        #Atributos de la clase
        self.scene = spaceInvaders
        self.background = background
        self.ship = ship
        self.enemys = enemys
        self.shot = shot 
        self.enemyshot= enemyshot
        self.countEnemy = 0
        #Cantidad de enemigos que quedan por poner 
        self.n = n-1
        #Cantidad de enemigos 
        self.enemyslive = n
        #Vidas del jugador
        self.shiplives = 3

    #Función que agrega una nave enemiga en escena
    def addEnemy(self):
        self.countEnemy += 1
        if self.countEnemy == 10:
            self.countEnemy = 0
            a = randint(0,10)

            if a == 0:
                a = randint(0,9)
                a /= 10
                self.enemys.createEnemy(a)
                self.n -= 1

    #Función que agrega una disparo en escena
    def addShot(self):
        self.shot.createShot(self.ship)

    #Función que agrega una disparo enemigo en escena
    def addEnemyShot(self):
        self.enemyshot.createEnemyShot(self.enemys)

    #Función que, dado un índice, elimina al enemigo asociado al índice
    def eliminateEnemys(self,i):
        self.enemys.removeEnemys(i)

    #Función que, dado un índice, elimina al disparo asociado al índice
    def eliminateShot(self,i):
        self.shot.removeShot(i)

    #Función que, dado un índice, elimina al disparo enemigo asociado al índice
    def eliminateEnemyShot(self,i):
        self.enemyshot.removeEnemyShot(i)

    #Función que verifica si un disparo del jugador colisiona con una nave enemiga
    def crashShotEnemy(self):
        for i in range(len(self.shot.y)):
            for j in range(len(self.enemys.y)):
                if self.shot.y[i] > self.enemys.y[j] -0.01 and self.shot.y[i] < self.enemys.y[j] + 0.01:
                    if self.shot.x[i] > self.enemys.x[j] - 0.05 and self.shot.x[i] < self.enemys.x[j] + 0.05:
                        #En caso de existir colisión, se elimina el disparo y la nave enemiga de la pantalla
                        self.eliminateEnemys(j)
                        self.eliminateShot(i)
                        self.enemyslive -=1
                        return

    #Función que verifica si un disparo del jugador colisiona con un disparo enemigo
    def crashShotEnemyShot(self):
        for i in range(len(self.shot.y)):
            for j in range(len(self.enemyshot.y)):
                if self.shot.y[i] > self.enemyshot.y[j] -0.05 and self.shot.y[i] < self.enemyshot.y[j] + 0.05:
                    if self.shot.x[i] > self.enemyshot.x[j] - 0.05 and self.shot.x[i] < self.enemyshot.x[j] + 0.05:

                        #En caso de existir colisión, se elimina el disparo y la nave enemiga de la pantalla
                        self.eliminateShot(i)
                        self.eliminateEnemyShot(j)
                        return

    #Función que verifica si un disparo enemigo colisiona colisiona con la nave del jugador
    def crashEnemyShotShip(self):
        for i in range(len(self.enemyshot.y)):
            if self.enemyshot.y[i] > self.ship.y -0.05 and self.enemyshot.y[i] < self.ship.y + 0.05:
                if self.enemyshot.x[i] > self.ship.x - 0.05 and self.enemyshot.x[i] < self.ship.x + 0.05:
                    #En caso de existir colisión, se elimina el disparo enemigo de la pantalla y el jugador pierde una vida 
                    self.eliminateEnemyShot(i)
                    self.shiplives -= 1
                    return


    #Función que actualiza la escena
    def update(self,dx,dy,shot):
        #Si el jugador disparo, se agrega una bala
        if shot == True:
            self.addShot()
        #Si quedan enemigos por agregar, se agrega un nuevo enemigo en pantalla
        if self.n > 0:
            self.addEnemy()

        #Se agregan los disparos enemigos
        self.addEnemyShot()

        #Se actualizan los elementos de la escena
        self.background.update()
        self.ship.update(dx,dy,shot)
        self.enemys.update()
        self.shot.update()
        self.enemyshot.update()
        
        #Se revisan las colisiones
        self.crashShotEnemy()
        self.crashShotEnemyShot()
        self.crashEnemyShotShip()

        #Se actualiza la escena
        self.scene.childs = [self.background.node, self.ship.node]
        self.scene.childs += self.enemys.nodes
        self.scene.childs += self.shot.nodes
        self.scene.childs += self.enemyshot.nodes


