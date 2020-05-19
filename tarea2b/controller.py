import glfw
import numpy as np
from libs import transformations as tr


# A class to store camera parameters.
class PolarCamera:

    # Initializing a Camera which moves with polar coordinates 
    def __init__(self):
        self.eyeX = -30
        self.eyeY = 0
        self.eyeZ = 5
        self.atX = 0
        self.atY = 0
        self.atZ = 1
        self.viewPos = 0.0
        self.view = 0.0
    
    def updateAt(self,x,y):
        self.atX = x
        self.atY = y

    def updateEye(self):
        self.eyeX = -30 + self.atX
        self.eyeY = self.atY

    def update_view(self):
        self.viewPos = np.array([self.eyeX, self.eyeY, self.eyeZ])
        
        self.view = tr.lookAt(
            self.viewPos,
            np.array([self.atX,self.atY,1]),
            np.array([0,0,1])
        )   
        
        return self.view

    def view_pos(self):
        return self.viewPos

# A class to store the application control
class Controller:
    def __init__(self):
        self.fillPolygon = True
        self.polar_camera = PolarCamera()
        self.r = 0
        self.theta = 0

    def camera(self):
        """ Get a camera reference from the controller object. """
        return self.polar_camera

# We will use the global controller as communication with the callback function
controller = Controller()
controller.polar_camera = PolarCamera()
camera = controller.polar_camera


def on_key(window, key, scancode, action, mods):

    global controller
    
    if action == glfw.PRESS:

        if key == glfw.KEY_ESCAPE:
            glfw.set_window_should_close(window,True)
    return 

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

    elif (glfw.get_key(window, glfw.KEY_DOWN) == glfw.PRESS):
        controller.r = -1
    else:
        controller.r = 0



