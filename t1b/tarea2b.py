import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import sys
import os
from PIL import Image

import basic_shapes as bs
import transformations as tr
import easy_shaders as es
import scene_graph as sg

# naves = sys.argv[1]

# A class to store the application control
class Controller:
    def __init__(self):
        #Movimiento en el eje x
        self.dx = 0
        #Movimiento en el eje y
        self.dy = 0

    def mod(self):
        if controller.dx < -1:
            controller.dx = 1
        if controller.dx > 1: 
            controller.dx = -1
        if controller.dy > 2:
            controller.dy = -2
        if controller.dy < -2:
            controller.dy = 2

# global controller as communication with the callback function
controller = Controller()

def on_key(window, key, scancode, action, mods):
    if action != glfw.PRESS:
        return

    global controller

    #Al apretar la tecla W, la nave se mueve hacia arriba en el espacio 
    if key == glfw.KEY_W:
        controller.dy += -0.05

    #Al apretar la tecla S, la nave se mueve hacia abajo en el espacio 
    elif key == glfw.KEY_S:
        controller.dy += 0.05

    #Al apretar la tecla D, la nave se mueve hacia la derecha
    elif key == glfw.KEY_D:
        controller.dx += 0.1

    #Al apretar la tecla A, la nave se mueve hacia la izquierda
    elif key == glfw.KEY_A:
        controller.dx += -0.1

    #Al apretar la tecla ESCAPE, se cierra la ventana y termina el programa
    elif key == glfw.KEY_ESCAPE:
        sys.exit()

    else:
        print("Unknown key")

    controller.mod()

#Función principal
if __name__ == "__main__":

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

    # A simple shader program with position and texture coordinates as inputs.
    pipeline = es.SimpleTextureTransformShaderProgram()
    
    # Telling OpenGL to use our shader program
    glUseProgram(pipeline.shaderProgram)

    # Setting up the clear screen color
    glClearColor(0.1, 0.1, 0.1, 1.0)

    # Enabling transparencies
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    # Se crean las figuras en la memoria GPU
    ## Fondo
    gpuBackground= es.toGPUShape(bs.createTextureQuad("images/background1.jpg"), GL_REPEAT, GL_NEAREST)
    ## Nave jugador
    gpuShip= es.toGPUShape(bs.createTextureQuad("images/ship.png"), GL_REPEAT, GL_NEAREST)

    #Scene graph
    ##Fondo
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
    
    ##Nave jugador
    ship = sg.SceneGraphNode("ship")
    ship.transform = tr.uniformScale(0.1)
    ship.childs = [gpuShip]
    
    ##Nave jugador trasladada
    translatedShip = sg.SceneGraphNode("translatedShip")
    translatedShip.transform = tr.translate(0, -0.9,0)
    translatedShip.childs = [ship]
    
    #Escena completa
    spaceInvaders = sg.SceneGraphNode("spaceInvader")
    spaceInvaders.childs = [scrollingBackground, translatedShip]
    
    #Se genera la animación
    while not glfw.window_should_close(window):
        #Para lograr el efecto del infinte scroll se necesita que se cumpla que: -2 < controller.dy < 2
        #Para lograr que la nave cruce la pantalla horizontalmente por un lado y aparezca en el otro se necesita que siempre se cumpla que: -1 < controller.dx < 2
        #Las dos condiciones mencionadas anteriormente son manejas por la llamada controller.mod()
        
        

        # Using GLFW to check for input events
        glfw.poll_events()
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

        # Clearing the screen in both, color and depth
        glClear(GL_COLOR_BUFFER_BIT)

        #Se mueve la nave, dependiendo del valor controller.dx
        ship = sg.findNode(spaceInvaders, "translatedShip")
        ship.transform = tr.translate(controller.dx,-0.9,0)

        #Se mueve el fondo, dependiendo del valor controller.dx
        background1 = sg.findNode(spaceInvaders, "translatedBackground1")
        background1.transform = tr.translate(0,controller.dy,0)

        #Se completa el espacio vacío generado por el movimiento del fondo
        if controller.dy > 0:
            background2 = sg.findNode(spaceInvaders, "translatedBackground2")
            background2.transform = tr.translate(0,-2+ controller.dy,0)
        else:
            background2 = sg.findNode(spaceInvaders, "translatedBackground2")
            background2.transform = tr.translate(0,2 + controller.dy,0)
 


        sg.drawSceneGraphNode(spaceInvaders, pipeline,"transform")
        # Once the render is done, buffers are swapped, showing only the complete scene.
        glfw.swap_buffers(window)

    glfw.terminate()
