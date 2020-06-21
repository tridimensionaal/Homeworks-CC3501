from OpenGL.GL import *
import numpy as np

from libs import basic_shapes as bs
from libs import transformations as tr
from libs import easy_shaders as es
from libs import scene_graph as sg
from libs import local_shapes as ls
from libs import nonuniform_splines as no

#Clase que se encaga de cargar la textura del skybox, generar el skybox y guardar la información de éste. 
class Skybox:
    def __init__(self):
        gpuSky = es.toGPUShape(bs.createTextureNormalsCube("images/sky.jpg"),GL_REPEAT, GL_LINEAR)

        sky = sg.SceneGraphNode("sky")
        sky.childs = [gpuSky]
        sky.transform = tr.uniformScale(2000)

        self.node = sky

#Clase que se encaga de cargar la textura de la pista, crear los puntos iniciales de la pista, generar la pista dado los puntos iniciales y guardar la información de ésta
class Track:
    def __init__(self):
        #Puntos que iniciales que definen la curva 
        p0 = np.array([8,0,0.3])
        p1 = np.array([5,6,0])
        p2 = np.array([3,3,0])
        p3 = np.array([0,7,0])
        p4 = np.array([-3,3,0.3])
        p5 = np.array([-5,6,0.3])
        p6 = np.array([-8,0,0.3])
        p7 = np.array([-5,-6,0])
        p8 = np.array([-3,-3,0])
        p9 = np.array([0,-7,0])
        p10 = np.array([3,-3,0.3])
        p11 = np.array([5,-6,0.3])

        points = np.array([p0,p1,p2,p3,p4,p5,p6,p7,p8,p9,p10,p11])

        #Se genera la clase que, dado los puntos iniciales, crea una nonuniform spline y almacena la información sobre la geometría de la pista.
        pointstrack = no.Track(points,300,100)

        #Dado la clase que almacena la información sobre la geometría de la pista, se crea el shape de la pista
        shapeTrack = ls.generateNormalTrack(pointstrack,"images/blue.png")

        gpuTrack = es.toGPUShape(shapeTrack, GL_REPEAT, GL_LINEAR)
        track = sg.SceneGraphNode("track")
        track.childs = [gpuTrack]

        self.node = track
        #Puntos del borde exterior de la pista
        self.points1 = pointstrack.ext
        #Puntos del borde interior de la pista
        self.points2 = pointstrack.int

#Clase que se encaga de cargar la textura del sol, generar el sol y guardar la información de éste.
class Sun:
    def __init__(self):
        gpuSphere= es.toGPUShape(ls.generateNormalSphere(30,30,"images/sun.png"), GL_REPEAT, GL_LINEAR)

        sphere = sg.SceneGraphNode("sphere")
        sphere.transform = tr.uniformScale(300)
        sphere.childs = [gpuSphere]

        rotatesphere = sg.SceneGraphNode("rotatesphere")
        rotatesphere.childs = [sphere]

        self.node = rotatesphere
        self.theta = 0
        self.dtheta = 0.001

    #Función que genera la rotación del solo sobre sí mismo.
    def update(self):
        self.theta += self.dtheta

        if self.theta > 2*np.pi:
            self.theta = 0

        self.node.transform = tr.rotationZ(self.theta)

#Clase que se encaga de cargar la textura de las cajas que marcan el inicio de la pista, generar las cajas y guardar la información de éstas.
class Boxes:
    #Se inicializa las cajas dado el auto, ya que se quiere que las cajas estén al inicio (donde el auto se encuentra inicialmente)
    def __init__(self,car):
        gpuBox  = es.toGPUShape(bs.createTextureNormalsCube("images/jalape.png"),GL_REPEAT, GL_LINEAR)

        box1 = sg.SceneGraphNode("box1")
        box1.transform = tr.uniformScale(10)
        box1.childs = [gpuBox]

        translatedbox1 = sg.SceneGraphNode("translatedbox1")
        translatedbox1.childs = [box1]

        box2 = sg.SceneGraphNode("box2")
        box2.transform = tr.uniformScale(10)
        box2.childs = [gpuBox]

        translatedbox2= sg.SceneGraphNode("translatedbox1")
        translatedbox2.childs = [box2]

        group = sg.SceneGraphNode("box")
        group.childs = [translatedbox1, translatedbox2]

        self.node = group
        self.x = car.x
        self.y = car.y
        self.z = car.z
        self.theta = 0
        self.dtheta = np.pi/200

    #Función que genera la rotación de las cajas sobre sí mismas.
    def update(self):
        self.theta += self.dtheta
        if self.theta > 2*np.pi:
            self.theta = 0

        box1 = self.node.childs[0]
        box2 = self.node.childs[1]

        box1.transform = tr.matmul([tr.translate(self.x+40, self.y+60,self.z), tr.rotationZ(self.theta)])
        box2.transform = tr.matmul([tr.translate(self.x-50,self.y+60,self.z),tr.rotationZ(-self.theta)])
        self.node.childs = [box1,box2]

#Clase que se encaga de cargar las texturas del auto, generar el auto, guardar la información de éste y proveer la lógica para que este se mueva.
class Car:
    #Se inicializa el auto dada la pista, ya que se quiere que el auto parta al inicio de la pista 
    def __init__(self,track):
        
        gpuSphere= es.toGPUShape(ls.generateNormalSphere(30,30,"images/pink1.jpeg"), GL_REPEAT, GL_LINEAR)
        gpuWheel = es.toGPUShape(ls.generateTextureNormalsCylinder(20,"images/black.jpg",2,1,0),GL_REPEAT, GL_LINEAR)

        gpuHead = es.toGPUShape(bs.createTextureNormalsCube("images/carita.jpg"),GL_REPEAT, GL_NEAREST)

        gpuSphere1 = es.toGPUShape(ls.generateNormalSphere(30,30,"images/green.png"), GL_REPEAT, GL_LINEAR)

        #Se crea la cabeza del auto
        head = sg.SceneGraphNode("head")
        head.transform = tr.uniformScale(4)
        head.childs = [gpuHead]

        translatedHead = sg.SceneGraphNode("traslatedHead")
        translatedHead.transform = tr.translate(0,0,4)
        translatedHead.childs = [head]

        #Se crea el cuerpo del auto
        sphere = sg.SceneGraphNode("sphere")
        sphere.transform = tr.uniformScale(3)
        sphere.childs = [gpuSphere]

        sphere1 = sg.SceneGraphNode("sphere1")
        sphere1.transform = tr.translate(0,0,8)
        sphere1.childs = [gpuSphere1]

        #Se crea las ruedas del auto
        leftwheel = sg.SceneGraphNode("leftwheel")
        leftwheel.childs = [gpuWheel]

        rightwheel= sg.SceneGraphNode("rightwheel")
        rightwheel.childs = [gpuWheel]

        rotateleftwheel = sg.SceneGraphNode("rotateleftwheel")
        rotateleftwheel.transform = tr.rotationX(np.pi/2)
        rotateleftwheel.childs = [leftwheel]

        rotaterightwheel= sg.SceneGraphNode("rotaterightwheel")
        rotaterightwheel.transform = tr.rotationX(-np.pi/2)
        rotaterightwheel.childs = [rightwheel]

        translatedleftwheel = sg.SceneGraphNode("translatedleftwheel")
        translatedleftwheel.transform = tr.translate(0,-3,-1)
        translatedleftwheel.childs = [rotateleftwheel]

        translatedrightwheel = sg.SceneGraphNode("translatedrightwheel")
        translatedrightwheel.transform = tr.translate(0,3,-1)
        translatedrightwheel.childs = [rotaterightwheel]

        group1 = sg.SceneGraphNode("group1")
        group1.childs = [sphere1, translatedHead, sphere]

        group2 = sg.SceneGraphNode("group2")
        group2.childs = [translatedleftwheel, translatedrightwheel]

        group = sg.SceneGraphNode("group1")
        group.transform = tr.translate(0,0,3)
        group.childs = [group1,group2]

        self.node = group
        #Posición inicial del auto
        self.x = (track.points1[0][0]+ track.points2[0][0])/2
        self.y = (track.points1[0][1]+ track.points2[0][1])/2
        self.z = (track.points1[0][2]+ track.points2[0][2])/2 + 3
        #Velocidad del auto
        self.r = 0
        #Aceleración del auto
        self.dr = 0.05
        #Aceleración respecto a z
        self.dzu = 0.065
        self.dzd =  self.dzu/2
        self.theta = np.pi/2
        #Velocidad de rotación del auto
        self.dtheta = np.pi/100
        self.phi = 0

    #Función que, dado un r, actualiza la velocidad 
    def updateR(self,r):
        if r == 0:
            self.r -= self.dr
            if self.r < 0:
                self.r = 0
        else:
            self.r += self.dr
            if self.r > 3:
                self.r = 3

    #Función que, dado un theta, actualiza el ángulo de rotación
    def updateTheta(self, theta):
        if theta == -1:
            self.theta -= self.dtheta

        elif theta == 0:
            pass
        else:
            self.theta += self.dtheta

    def updateZ(self):
        if self.r > 0:
            if self.x*self.y > 0:
                self.z -= self.r*self.dzd
                if self.z < 3.2:
                    self.z = 3.2
            else:
                self.z += self.r*self.dzu
                if self.z > 36.5:
                    self.z = 36.5
        else:
            pass

 
 
    def updateWheels(self):
        self.phi -= 0.75*self.r
        leftwheel = sg.findNode(self.node,"leftwheel")
        leftwheel.transform = tr.rotationZ(self.phi)

        rightwheel = sg.findNode(self.node,"rightwheel")
        rightwheel.transform = tr.rotationZ(self.phi)
 
    def update(self,r,theta):
        self.updateR(r)
        self.updateTheta(theta)
        self.updateZ()
        self.updateWheels()

        self.x +=  self.r*np.cos(self.theta)
        self.y += self.r*np.sin(self.theta)
        group = self.node 
        group1 = group.childs[0]
        group2 = group.childs[1]


        group1.transform = tr.rotationZ(self.theta)
        group2.transform = tr.rotationZ(self.theta)
        group.transform = tr.translate(self.x,self.y,self.z)

class Scene:
    def __init__(self):
        track = Track()
        car = Car(track)
        sky = Skybox()
        box = Boxes(car)
        sun = Sun()

        scene = sg.SceneGraphNode("scene")

        self.node = scene
        self.track = track
        self.car = car
        self.sky = sky
        self.box = box
        self.sun = sun

    def update(self, r,theta):
        self.car.update(r,theta)
        self.box.update()
        self.sun.update()

        self.node.childs = [self.track.node, self.car.node, self.sky.node, self.box.node, self.sun.node]



