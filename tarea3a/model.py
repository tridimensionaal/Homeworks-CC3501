from OpenGL.GL import *
import numpy as np
from random import randint

from libs import basic_shapes as bs
from libs import transformations as tr
from libs import easy_shaders as es
from libs import scene_graph as sg
from libs import local_shapes as ls

class Aquarium:
    def __init__(self,temp):
        dimensions = temp.shape
        x = dimensions[0]
        y = dimensions[1]
        z = dimensions[2]

        gpuAquarium =  es.toGPUShape(bs.createTextureNormalsCube("images/water.jpg"),GL_REPEAT, GL_LINEAR)

        aquarium = sg.SceneGraphNode("aquarium")
        aquarium.childs = [gpuAquarium]
        aquarium.transform = tr.scale(x+1,y+1,z+1)

        translatedAquarium = sg.SceneGraphNode("translatedAquarium")
        translatedAquarium.childs = [aquarium]
        translatedAquarium.transform = tr.translate(x/2,y/2,z/2)

        self.x = x
        self.y = y
        self.z = z
        self.temp = temp 
        self.ocup = np.zeros((x,y,z))
        self.node = translatedAquarium

class Voxeles:
    def __init__(self,aquarium,ta,tb,tc):
        gpuVoxelTa =  es.toGPUShape(bs.createTextureNormalsCube("images/water.jpg"),GL_REPEAT, GL_LINEAR)
        gpuVoxelTb=  es.toGPUShape(bs.createTextureNormalsCube("images/water.jpg"),GL_REPEAT, GL_LINEAR)
        gpuVoxelTc =  es.toGPUShape(bs.createTextureNormalsCube("images/water.jpg"),GL_REPEAT, GL_LINEAR)

        x = aquarium.x
        y = aquarium.y
        z = aquarium.z

        voxelesTa = []
        voxelesTb = []
        voxelesTc = []

        voxelesTaPos= []
        voxelesTbPos= []
        voxelesTcPos = []

        for i in range(x):
            for j in range(y):
                for k in range(z):
                    if ta-2 <= aquarium.temp[i][j][k] <= ta+2:
                        #Se crea un voxel
                        voxelTa = sg.SceneGraphNode("voxelTa")
                        voxelTa.childs = [gpuVoxelTa]
                        voxelTa.transform = tr.translate(i,j,k)

                        voxelesTa += [voxelTa]
                        voxelesTaPos+= [[i,j,k]]

                    if tb-2 <= aquarium.temp[i][j][k] <= tb+2:
                        voxelTb= sg.SceneGraphNode("voxelTb")
                        voxelTb.childs = [gpuVoxelTb]
                        voxelTb.transform = tr.translate(i,j,k)

                        voxelesTb += [voxelTb]
                        voxelesTbPos+= [[i,j,k]]

                    if tc-2 <= aquarium.temp[i][j][k] <= tc+2:
                        voxelTc= sg.SceneGraphNode("voxelTc")
                        voxelTc.childs = [gpuVoxelTc]
                        voxelTc.transform = tr.translate(i,j,k)

                        voxelesTc += [voxelTc]
                        voxelesTcPos+= [[i,j,k]]
 
        self.node = sg.SceneGraphNode("node")
        self.voxelesTa = voxelesTa
        self.voxelesTb = voxelesTb
        self.voxelesTc = voxelesTc
        self.voxelesTaPos = voxelesTaPos
        self.voxelesTbPos = voxelesTbPos
        self.voxelesTcPos = voxelesTcPos



    def update(self,a,b,c):
        self.node.childs = []
        if a==1:
            self.node.childs += self.voxelesTa
        if b==1:
            self.node.childs += self.voxelesTb
        if c==1:
            self.node.childs += self.voxelesTc

class Fishes:
    def __init__(self):
        #Cuerpo y elementos cola pez tipo A
        gpuSphereA= es.toGPUShape(ls.generateNormalSphere(30,30,"images/pink1.jpeg"), GL_REPEAT, GL_LINEAR)
        #Cola pez tipo A
        gpuCylinderA = es.toGPUShape(ls.generateTextureNormalsCylinder(20,"images/pink1.jpeg",1,2,0),GL_REPEAT, GL_LINEAR)

        #Cuerpo y elementos cola pez tipo B
        gpuSphereB = es.toGPUShape(ls.generateNormalSphere(30,30,"images/green.png"), GL_REPEAT, GL_LINEAR)
        #Cola pez tipo B
        gpuCylinderB = es.toGPUShape(ls.generateTextureNormalsCylinder(20,"images/green.png",1,2,0),GL_REPEAT, GL_LINEAR)

        #Cuerpo y elementos cola pez tipo C
        gpuSphereC = es.toGPUShape(ls.generateNormalSphere(30,30,"images/black.jpg"), GL_REPEAT, GL_LINEAR)
        #Cola pez tipo c
        gpuCylinderC = es.toGPUShape(ls.generateTextureNormalsCylinder(20,"images/black.jpg",1,2,0),GL_REPEAT, GL_LINEAR)


        self.gpuSphereA = gpuSphereA
        self.gpuCylinderA = gpuCylinderA

        self.gpuSphereB = gpuSphereB
        self.gpuCylinderB = gpuCylinderB

        self.gpuSphereC= gpuSphereC
        self.gpuCylinderC = gpuCylinderC

        self.node = sg.SceneGraphNode("node")

        self.theta = 0
        self.dtheta = np.pi/400

    def create(self, t,x,y,z):
        if t == 1:
            gpuSphere = self.gpuSphereA
            gpuCylinder = self.gpuCylinderA

        elif t == 2:
            gpuSphere = self.gpuSphereB
            gpuCylinder = self.gpuCylinderB
        else:
            gpuSphere = self.gpuSphereC
            gpuCylinder = self.gpuCylinderC
            
        #Se crea el cuerpo del pez
        body = sg.SceneGraphNode("body")
        body.childs = [gpuSphere]

        #Se crea la cola
        tail = sg.SceneGraphNode("tail")
        tail.childs = [gpuCylinder]
        tail.transform = tr.rotationY(np.pi/2)

        #Se escala la cola
        scaledTail = sg.SceneGraphNode("scaledTail")
        scaledTail.childs = [tail]
        scaledTail.transform = tr.uniformScale(0.5)

        #Se traslada la cola
        translatedTail = sg.SceneGraphNode("translatedTail")
        translatedTail.childs = [scaledTail]
        translatedTail.transform = tr.translate(0.5,0,0)

        #Se crea el final de la cola
        elementTail = sg.SceneGraphNode("elementTail")
        elementTail.childs = [gpuSphere]
        elementTail.transform = tr.uniformScale(0.5)

        #Se crea el final de la cola
        translatedElementTail = sg.SceneGraphNode("translatedElementTail")
        translatedElementTail.childs = [elementTail]
        translatedElementTail.transform = tr.translate(1.7,0,0)

        group = sg.SceneGraphNode("group")
        group.childs = [translatedElementTail, translatedTail]

        fish = sg.SceneGraphNode("fish")
        fish.childs = [group, body]
        fish.transform = tr.uniformScale(0.5)

        translatedFish = sg.SceneGraphNode("fish")
        translatedFish.childs = [fish]
        translatedFish.transform = tr.translate(x,y,z)

        self.node.childs += [translatedFish]

    def update(self):
        self.theta += self.dtheta

        if self.theta > np.pi/32 or self.theta < -np.pi/32:
            self.dtheta = -self.dtheta

        for fish in self.node.childs:
            group = sg.findNode(fish, "group")
            group.transform = tr.rotationZ(self.theta)

class Scene:
    def __init__(self,data,aquarium):
        ta = data["t_a"]
        tb = data["t_b"]
        tc = data["t_c"]
        na = data["n_a"]
        nb = data["n_b"]
        nc = data["n_c"]

        aquarium = Aquarium(aquarium)
        voxeles = Voxeles(aquarium,ta,tb,tc)
        fishes = Fishes()


        for i in range(na):
            positions = voxeles.voxelesTaPos

            if len(positions) > 0:
                j = randint(0,len(positions)-1)
                pos = positions.pop(j)
                fishes.create(1,pos[0],pos[1],pos[2])
            else:
                break

        for i in range(nb):
            positions = voxeles.voxelesTbPos

            if len(positions) > 0:
                j = randint(0,len(positions)-1)
                pos = positions.pop(j)
                fishes.create(2,pos[0],pos[1],pos[2])
            else:
                break

        for i in range(nc):
            positions = voxeles.voxelesTcPos

            if len(positions) > 0:
                j = randint(0,len(positions)-1)
                pos = positions.pop(j)
                fishes.create(3,pos[0],pos[1],pos[2])
            else:

                break

        self.aquarium = aquarium
        self.voxeles = voxeles
        self.fishes = fishes

    def update(self,a,b,c):
        self.fishes.update()
        self.voxeles.update(a,b,c)
