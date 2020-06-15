from OpenGL.GL import *
import numpy as np

from libs import basic_shapes as bs
from libs import transformations as tr
from libs import easy_shaders as es
from libs import scene_graph as sg
from libs import local_shapes as ls

class Car:
    def __init__(self):
        
        gpuSphere= es.toGPUShape(ls.generateNormalSphere(30,30,"images/pink1.jpg"), GL_REPEAT, GL_LINEAR)
        gpuWheel = es.toGPUShape(ls.generateTextureNormalsCylinder(20,"images/black1.png",2,1,0),GL_REPEAT, GL_LINEAR)

        gpuHead = es.toGPUShape(bs.createTextureNormalsCube("images/carita.jpg"),GL_REPEAT, GL_LINEAR)

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
        group.transform = tr.matmul([tr.translate(0,0,0),tr.rotationZ(0)])
        group.childs = [translatedHead, sphere, translatedleftwheel, translatedrightwheel]

        self.node = group
        self.x = 0
        self.y = 0
        self.z = 0
        self.r = 0
        self.dr = 0.05
        self.theta = 0
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
            if self.r > 0.75:
                self.r = 0.75

    def updateTheta(self, theta):
        if theta == -1:
            self.theta -= self.dtheta
            if self.theta < -np.pi/2:
                self.theta = -np.pi/2

        elif theta == 0:
            if self.theta > 0:
                self.theta -= self.dtheta
                if self.theta < 0:
                    self.theta = 0

            elif self.theta < 0:
                self.theta += self.dtheta
                if self.theta > 0:
                    self.theta = 0
        else:
            self.theta += self.dtheta
            if self.theta > np.pi/2:
                self.theta = np.pi/2


    def update(self,r,theta):
        self.updateR(r)
        self.updateTheta(theta)

        self.x +=  self.r*np.cos(self.theta)
        self.y += self.r*np.sin(self.theta)
        group = self.node 
        group.transform = tr.matmul([tr.translate(self.x,self.y,self.z),tr.rotationZ(self.theta)])
 









