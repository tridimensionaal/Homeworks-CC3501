import glfw
import numpy as np
from libs import transformations as tr


#Clase que almacena los parámetros de la cámara
class PolarCamera:

    #Se inicializa la cámara con sus distintos atributos
    def __init__(self):
        self.eyeX = 0
        self.eyeY = 0
        self.eyeZ = 0 
        self.atX = 0
        self.atY = 0
        self.atZ = 0
        self.viewPos = 0
        self.view = 0

    #Función que, dado valores, x, y, z, actualiza la posición del at
    def updateAt(self,x,y,z):
        self.atX = x
        self.atY = y
        self.atZ = z+20

    #Función que, dado un ángulo alpha actualiza la posición del eye
    def updateEye(self,alpha):
        self.eyeX = -(100)*np.cos(alpha)+ self.atX
        self.eyeY = self.atY  - (100)*np.sin(alpha)
        self.eyeZ = self.atZ + 5

    #Función que actualiza la vista
    def update_view(self):
        self.viewPos = np.array([self.eyeX, self.eyeY, self.eyeZ])
        
        self.view = tr.lookAt(
            self.viewPos,
            np.array([self.atX,self.atY,1]),
            np.array([0,0,3])
        )   
        
        return self.view

    #Función que retorna la posición del eye
    def view_pos(self):
        return self.viewPos

#Clase que almacena la aplicación de control
class Controller:
    #Se inicializa la aplicación de control con sus distintos atributos
    def __init__(self):
        self.fillPolygon = True
        self.polar_camera = PolarCamera()
        self.r = 0
        self.theta = 0

    #Función que retorna la cámara
    def camera(self):
        return self.polar_camera

#Se inicializa la aplicación de control y la cámara
controller = Controller()
controller.polar_camera = PolarCamera()
camera = controller.polar_camera

#
def on_key(window, key, scancode, action, mods):

    global controller
    
    if action == glfw.PRESS:

        if key == glfw.KEY_ESCAPE:
            glfw.set_window_should_close(window,True)
    return 

#Función que dada una ventana, recibe los inputs de teclados correspondientes
def key2(window):
    global controller 

    if (glfw.get_key(window, glfw.KEY_LEFT) == glfw.PRESS):
        controller.theta = 1

    elif (glfw.get_key(window, glfw.KEY_RIGHT) == glfw.PRESS):
        controller.theta = -1
    else:
        controller.theta = 0


    if (glfw.get_key(window, glfw.KEY_UP) == glfw.PRESS):
        controller.r = 1
    else:
        controller.r = 0



