from OpenGL.GL import *
import numpy as np

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
        aquarium.transform = tr.scale(x,y,z)

        translatedAquarium = sg.SceneGraphNode("translatedAquarium")
        translatedAquarium.childs = [aquarium]
        translatedAquarium.transform = tr.translate(x/2,y/2,z/2)

        self.x = x
        self.y = y
        self.z = z
        self.temp = temp 
        self.ocup = np.zeros((x,y,z))
        self.node = translatedAquarium

class Fish:
    def __init__(self,aquarium):
        #Cuerpo y elementos cola
        gpuSphere= es.toGPUShape(ls.generateNormalSphere(30,30,"images/pink1.jpeg"), GL_REPEAT, GL_LINEAR)
        #cola
        gpuCylinder = es.toGPUShape(ls.generateTextureNormalsCylinder(20,"images/pink1.jpeg",1,2,0),GL_REPEAT, GL_LINEAR)

        #Se crea el cuerpo del pez
        body = sg.SceneGraphNode("body")
        body.childs = [gpuSphere]

        #
        tail = sg.SceneGraphNode("tail")
        tail.childs = [gpuCylinder]
        tail.transform = tr.rotationY(np.pi/2)

        scaledTail = sg.SceneGraphNode("scaledTail")
        scaledTail.childs = [tail]
        scaledTail.transform = tr.uniformScale(0.5)


        translatedTail = sg.SceneGraphNode("translatedTail")
        translatedTail.childs = [scaledTail]
        translatedTail.transform = tr.translate(0.5,0,0)

        elementTail = sg.SceneGraphNode("elementTail")
        elementTail.childs = [gpuSphere]
        elementTail.transform = tr.uniformScale(0.5)

        translatedElementTail = sg.SceneGraphNode("translatedElementTail")
        translatedElementTail.childs = [elementTail]
        translatedElementTail.transform = tr.translate(1.7,0,0)

        fish = sg.SceneGraphNode("fish")
        fish.childs = [translatedElementTail, translatedTail, body]
        fish.transform = tr.uniformScale(0.5)

        translatedFish = sg.SceneGraphNode("fish")
        translatedFish.childs = [fish]

        x = aquarium.x
        y = aquarium.y
        z = aquarium.z

        for i in range(1,x-1):
            for j in range(1,y-1):
                for k in range(1,z-1):
                    if aquarium.temp[i][j][k] > 13 and aquarium.temp[i][j][k] < 17:
                        if aquarium.ocup[i][j][k] == 0: 
                            x = i
                            y = j
                            z = k
                            break

        translatedFish.transform = tr.translate(x,y,z)

        self.node = translatedFish

class Scene:
    def __init__(self,data,aquarium):
        self.aquarium = Aquarium(aquarium)
        self.fish = Fish(self.aquarium)
    







