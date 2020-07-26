from OpenGL.GL import *
import numpy as np
from random import randint

from libs import basic_shapes as bs
from libs import transformations as tr
from libs import easy_shaders as es
from libs import scene_graph as sg
from libs import local_shapes as ls

#Clase que representa un acuario
class Aquarium:
    #Método para inicializar un objeto de la clase, dado una matriz temp con las temperaturas en el espacio
    def __init__(self,temp):
        dimensions = temp.shape
        x = dimensions[0]
        y = dimensions[1]
        z = dimensions[2]

        #Se carga la textura para el acuario y se genera un cubo con ésta
        gpuAquarium =  es.toGPUShape(bs.createTextureNormalsCube("images/water.jpg"),GL_REPEAT, GL_LINEAR)

        #Se crea el nodo del acuario
        aquarium = sg.SceneGraphNode("aquarium")
        aquarium.childs = [gpuAquarium]
        aquarium.transform = tr.scale(x,y,z)

        #Se traslada el acuario a su posición correspondiente
        translatedAquarium = sg.SceneGraphNode("translatedAquarium")
        translatedAquarium.childs = [aquarium]
        translatedAquarium.transform = tr.translate(x/2,y/2,z/2)
        
        #Paramétros de los objetos de la clase
        self.x = x
        self.y = y
        self.z = z
        self.temp = temp 
        self.node = translatedAquarium

#Clase que representa el conjunto de voxeles
class Voxeles:
    #Método que para inicializar un objeto de la clase, dado un objeto de la clase aquarium y tres temperaturas ta, tb, tc
    def __init__(self,aquarium,ta,tb,tc):
        x = aquarium.x
        y = aquarium.y
        z = aquarium.z

        voxelTa = bs.Shape([],[], "./images/pink1.jpeg")
        voxelTb = bs.Shape([],[], "./images/green.png")
        voxelTc = bs.Shape([],[], "./images/blue.png")

        #Se guardan las posiciones de los voxeles
        voxelesTaPos= []
        voxelesTbPos= []
        voxelesTcPos = []
        
        #Se recorren todos los puntos del acuario y, dado la temperatura de estos puntos, si el punto se encuentra en cualquiera de los tres rangos dados por las temperaturas ta, tb y tc, entonces se dibuja un voxel en aquel punto (voxel asociado a la temperatura del rango).
        for i in range(x):
            for j in range(y):
                for k in range(z):
                    if ta-2 <= aquarium.temp[i][j][k] <= ta+2:
                        temp_shape = bs.createTextureNormalsCube2(i,j,k,"./images/pink1.jpeg")
                        bs.merge(destinationShape=voxelTa, strideSize=6, sourceShape=temp_shape)
                        voxelesTaPos += [[i,j,k]]

                    if tb-2 <= aquarium.temp[i][j][k] <= tb+2:
                        temp_shape = bs.createTextureNormalsCube2(i,j,k,"./images/green.png")
                        bs.merge(destinationShape=voxelTb, strideSize=6, sourceShape=temp_shape)
                        voxelesTbPos += [[i,j,k]]

                    if tc-2 <= aquarium.temp[i][j][k] <= tc+2:
                        temp_shape = bs.createTextureNormalsCube2(i,j,k,"./images/black.jpg")
                        bs.merge(destinationShape=voxelTc, strideSize=6, sourceShape=temp_shape)
                        voxelesTcPos += [[i,j,k]]
 
        #Atributos de los objetos de la clase.
        self.voxelesTa = es.toGPUShape(voxelTa,GL_REPEAT, GL_LINEAR)
        self.voxelesTb = es.toGPUShape(voxelTb,GL_REPEAT, GL_LINEAR)
        self.voxelesTc = es.toGPUShape(voxelTc,GL_REPEAT, GL_LINEAR)
        self.voxelesTaPos = voxelesTaPos
        self.voxelesTbPos = voxelesTbPos
        self.voxelesTcPos = voxelesTcPos
        self.node = sg.SceneGraphNode("node")

    #Método 
    def update(self,a,b,c):
        node = sg.SceneGraphNode("node")
        if a==True:
            voxel = sg.SceneGraphNode("voxel")
            voxel.childs = [self.voxelesTa]

            node.childs += [voxel]
        if b==True:
            voxel = sg.SceneGraphNode("voxel")
            voxel.childs = [self.voxelesTb]
 
            node.childs += [voxel]
        if c==True:
            voxel = sg.SceneGraphNode("voxel")
            voxel.childs = [self.voxelesTc]
 
            node.childs += [voxel]
        self.node = node

#Clase que representa el conjunto de peces
class Fishes:

    #Método para inicializar un objeto de la clase
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
        gpuSphereC = es.toGPUShape(ls.generateNormalSphere(30,30,"images/blue.png"), GL_REPEAT, GL_LINEAR)
        #Cola pez tipo c
        gpuCylinderC = es.toGPUShape(ls.generateTextureNormalsCylinder(20,"images/blue.png",1,2,0),GL_REPEAT, GL_LINEAR)

        ##Atributos de los objetos de la clase
        #Partes básicas del pez A
        self.gpuSphereA = gpuSphereA
        self.gpuCylinderA = gpuCylinderA

        #Partes básicas del pez B
        self.gpuSphereB = gpuSphereB
        self.gpuCylinderB = gpuCylinderB

        #Partes básicas del pez C
        self.gpuSphereC= gpuSphereC
        self.gpuCylinderC = gpuCylinderC

        #Nodo que representa el conjunto de peces
        self.node = sg.SceneGraphNode("node")

        #Parámetros para generar una animación de los peces
        self.theta = 0
        self.dtheta = np.pi/400
    
    #Método para crear un pez dado un parámetro t que representa que tipo de pez se va a crear y dado los paramétros x,y,z que representan la posición del pez.
    def create(self, t,x,y,z):
        #Dependiendo del parámetro t, se define que tipo de pez se va a crear
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
        
        #Se juntan los elementos de la cola
        group = sg.SceneGraphNode("group")
        group.childs = [translatedElementTail, translatedTail]

        #Se juntan los elementos del pez
        fish = sg.SceneGraphNode("fish")
        fish.childs = [group, body]
        fish.transform = tr.uniformScale(0.5)
        
        #Se ubica el pez en su posición correspondiente
        translatedFish = sg.SceneGraphNode("fish")
        translatedFish.childs = [fish]
        translatedFish.transform = tr.translate(x,y,z)
        
        #Se agrega el pez al conjunto de peces.
        self.node.childs += [translatedFish]

    #Se genera la animación para cada pez del conjunto de peces
    def update(self):
        self.theta += self.dtheta

        if self.theta > np.pi/32 or self.theta < -np.pi/32:
            self.dtheta = -self.dtheta

        for fish in self.node.childs:
            group = sg.findNode(fish, "group")
            group.transform = tr.rotationZ(self.theta)

#Clase que representa la escena en su totalidad (acuario, peces y voxeles).
class Scene:

    #Método para inicializar un objeto de la clase, dado un diccionario que los setup de la visualización y dada una matriz con las temperaturas del acuario
    def __init__(self,data,aquarium):
        #Se inicia los datos de la visualziación
        ta = data["t_a"]
        tb = data["t_b"]
        tc = data["t_c"]
        na = data["n_a"]
        nb = data["n_b"]
        nc = data["n_c"]
        
        #Se crea un objeto de la clase aquarium
        aquarium = Aquarium(aquarium)
        #Se crea un objeto de la clase voxeles 
        voxeles = Voxeles(aquarium,ta,tb,tc)
        #Se crea un objeto de la clase 
        fishes = Fishes()

        #Se crean los peces de tipo a
        for i in range(na):
            positions = voxeles.voxelesTaPos

            if len(positions) > 0:
                j = randint(0,len(positions)-1)
                pos = positions.pop(j)
                fishes.create(1,pos[0],pos[1],pos[2])
            else:
                break

        #Se crean los peces de tipo b
        for i in range(nb):
            positions = voxeles.voxelesTbPos

            if len(positions) > 0:
                j = randint(0,len(positions)-1)
                pos = positions.pop(j)
                fishes.create(2,pos[0],pos[1],pos[2])
            else:
                break

        #Se crean los peces de tipo c
        for i in range(nc):
            positions = voxeles.voxelesTcPos

            if len(positions) > 0:
                j = randint(0,len(positions)-1)
                pos = positions.pop(j)
                fishes.create(3,pos[0],pos[1],pos[2])
            else:

                break

        #Atributos de los objetos de la clase
        self.aquarium = aquarium
        self.voxeles = voxeles
        self.fishes = fishes

    #
    def update(self,a,b,c):
        self.fishes.update()
        self.voxeles.update(a,b,c)
