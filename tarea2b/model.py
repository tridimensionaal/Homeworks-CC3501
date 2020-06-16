from OpenGL.GL import *
import numpy as np

from libs import basic_shapes as bs
from libs import transformations as tr
from libs import easy_shaders as es
from libs import scene_graph as sg
from libs import local_shapes as ls
class Track:
    def __init__(self):
        #Puntos que defines el borde exterior de la pista
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
        nodes1 = np.array([p0,p1,p2,p3,p4,p5,p6,p7,p8,p9,p10,p11])

        #Puntos que defines el borde interior de la pista
        p0 = np.array([7,0,0.3])
        p1 = np.array([5,4,0])
        p2 = np.array([3,1,0])
        p3 = np.array([0,5,0])
        p4 = np.array([-3,1,0.3])
        p5 = np.array([-5,4,0.3])
        p6 = np.array([-7,0,0.3])
        p7 = np.array([-5,-4,0])
        p8 = np.array([-3,-1,0])
        p9 = np.array([0,-5,0])
        p10 = np.array([3,-1,0.3])
        p11 = np.array([5,-4,0.3])
        nodes2 = np.array([p0,p1,p2,p3,p4,p5,p6,p7,p8,p9,p10,p11])

        points1, points2, shapeTrack = ls.generateNormalTrack(nodes1,nodes2,60,"images/blue.png")

        gpuTrack = es.toGPUShape(shapeTrack, GL_REPEAT, GL_LINEAR)
        track = sg.SceneGraphNode("track")
        track.childs = [gpuTrack]

        self.node = track
        self.points1 = points1 
        self.points2 = points2

class Skybox:
    def __init__(self):
        gpuSky = es.toGPUShape(bs.createTextureNormalsCube("images/sky.jpg"),GL_REPEAT, GL_LINEAR)

        sky = sg.SceneGraphNode("sky")
        sky.childs = [gpuSky]
        sky.transform = tr.uniformScale(2000)

        self.node = sky

class Car:
    def __init__(self,track):
        
        gpuSphere= es.toGPUShape(ls.generateNormalSphere(30,30,"images/pink1.jpg"), GL_REPEAT, GL_LINEAR)
        gpuWheel = es.toGPUShape(ls.generateTextureNormalsCylinder(20,"images/black1.png",2,1,0),GL_REPEAT, GL_LINEAR)

        gpuHead = es.toGPUShape(bs.createTextureNormalsCube("images/carita.jpg"),GL_REPEAT, GL_NEAREST)

        #
        head = sg.SceneGraphNode("head")
        head.transform = tr.uniformScale(4)
        head.childs = [gpuHead]

        translatedHead = sg.SceneGraphNode("traslatedHead")
        translatedHead.transform = tr.translate(0,0,4)
        translatedHead.childs = [head]

        #
        sphere = sg.SceneGraphNode("sphere")
        sphere.transform = tr.uniformScale(3)
        sphere.childs = [gpuSphere]

        #
        leftwheel = sg.SceneGraphNode("leftwheel")
        leftwheel.transform = tr.rotationX(np.pi/2)
        leftwheel.childs = [gpuWheel]

        rightwheel= sg.SceneGraphNode("rightwheel")
        rightwheel.transform = tr.rotationX(-np.pi/2)
        rightwheel.childs = [gpuWheel]

        translatedleftwheel = sg.SceneGraphNode("translatedleftwheel")
        translatedleftwheel.transform = tr.translate(0,-3,-1)
        translatedleftwheel.childs = [leftwheel]

        translatedrightwheel = sg.SceneGraphNode("translatedrightwheel")
        translatedrightwheel.transform = tr.translate(0,3,-1)
        translatedrightwheel.childs = [rightwheel]

        group = sg.SceneGraphNode("group")
        group.transform = tr.matmul([tr.translate(0,0,3),tr.rotationZ(0)])
        group.childs = [translatedHead, sphere, translatedleftwheel, translatedrightwheel]

        self.node = group
        self.x = (track.points1[0][0]+ track.points2[0][0])/2
        self.y = (track.points1[0][1]+ track.points2[0][1])/2
        self.z = (track.points1[0][2]+ track.points2[0][2])/2 + 3
        self.r = 0
        self.dr = 0.05
        self.dz = 0.05
        self.theta = np.pi/2
        self.dtheta = np.pi/100

    def updateR(self,r):
        if r == -1:
            self.r -= self.dr
            if self.r < -0.75:
                self.r = -0.75
        elif r == 0:
            self.r -= self.dr
            if self.r < 0:
                self.r = 0
        else:
            self.r += self.dr
            if self.r > 2:
                self.r = 2

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
                self.z -= self.r*self.dz
                if self.z < 3:
                    self.z = 3
            else:
                self.z += self.r*self.dz
                if self.z > 21:
                    self.z = 21
        else:
            return
            
    def update(self,r,theta):
        self.updateR(r)
        self.updateTheta(theta)
        self.updateZ()

        self.x +=  self.r*np.cos(self.theta)
        self.y += self.r*np.sin(self.theta)
        group = self.node 
        group.transform = tr.matmul([tr.translate(self.x,self.y,self.z+0.05),tr.rotationZ(self.theta)])
 
