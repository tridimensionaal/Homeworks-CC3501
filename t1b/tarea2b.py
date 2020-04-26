import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import sys
import os
from PIL import Image

from libs import easy_shaders as es
from libs import transformations as tr
from libs import scene_graph as sg

import model 
from controller import *

# naves = sys.argv[1]

#Función que genera una ventana y sus respectivas configuraciones
def windowConf():    
    #Setups para la ventana 

    # Initialize glfw
    if not glfw.init():
        sys.exit()

    #Tamaño de la ventana
    width = 900
    height = 600

    #Ventana
    window = glfw.create_window(width, height, "Space Invaders", None, None)

    if not window:
        glfw.terminate()
        sys.exit()

    glfw.make_context_current(window)

    # Connecting the callback function 'on_key' to handle keyboard events
    glfw.set_key_callback(window, on_key)

    # Setting up the clear screen color
    glClearColor(0.1, 0.1, 0.1, 1.0)

    # Enabling transparencies
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    return window 

#Función principal
if __name__ == "__main__":
    #Configuración de la ventana
    window = windowConf()

    # A simple shader program with position and texture coordinates as inputs.
    pipeline = es.SimpleTextureTransformShaderProgram()
    
    # Telling OpenGL to use our shader program
    glUseProgram(pipeline.shaderProgram)

    spaceInvaders = model.Model()
    #Se genera la animación
    while not glfw.window_should_close(window):

        controller.mod()

        # Using GLFW to check for input events
        glfw.poll_events()
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

        # Clearing the screen in both, color and depth
        glClear(GL_COLOR_BUFFER_BIT)

        #Se mueve la nave, dependiendo del valor controller.dx y controller.dy
        spaceInvaders.update(controller.dx,controller.dy)

        sg.drawSceneGraphNode(spaceInvaders.scene, pipeline,"transform")
        # Once the render is done, buffers are swapped, showing only the complete scene.
        glfw.swap_buffers(window)

    glfw.terminate()
