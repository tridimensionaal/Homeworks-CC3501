# coding=utf-8

import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import sys


from libs import transformations as tr
from libs import basic_shapes as bs
from libs import easy_shaders as es
from libs import lighting_shaders as light_s
from libs import local_shapes as ls
from libs import scene_graph as sg

from controller import *
import model 


width = 900
height = 600

#Función que genera una ventana y sus respectivas configuraciones
def windowConf():    
    #Setups para la ventana 

    # Initialize glfw
    if not glfw.init():
        sys.exit()

    #Tamaño de la ventana
    #Ventana
    window = glfw.create_window(width, height, "Crazy Race 3D", None, None)

    if not window:
        glfw.terminate()
        sys.exit()

    glfw.make_context_current(window)

    # Connecting the callback function 'on_key' to handle keyboard events
    glfw.set_key_callback(window, on_key)

    # Setting up the clear screen color
    glClearColor(0.7, 0.7, 0.7, 1.0)

    # Enabling transparencies
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    glEnable(GL_DEPTH_TEST)

    return window


if __name__ == "__main__":

    window = windowConf()

    # Assembling the shader program
    lightingPipeline = light_s.SimpleTextureGouraudShaderProgram()

    # As we work in 3D, we need to check which part is in front,
    # and which one is at the back

    # Creating shapes on GPU memory
    track = model.Track()
    car = model.Car(track)
    sky = model.Skybox()
    box = model.Boxes(car)
    sun = model.Sun()

    xl = car.x
    yl = car.y
    zl = car.z

    while not glfw.window_should_close(window):
        # Using GLFW to check for input events
        glfw.poll_events()
        key2(window)

        # Setting up the projection transform
        projection = tr.perspective(60, float(width)/float(height), 0.1, 2000)

        controller.camera().updateAt(car.x,car.y,car.z)
        controller.camera().updateEye(car.theta)
        view = controller.camera().update_view()
        viewPos = controller.camera().view_pos()

        # Clearing the screen in both, color and depth
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glUseProgram(lightingPipeline.shaderProgram)

        # White light in all components: ambient, diffuse and specular.
        glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "La"), 0.7, 0.7, 0.7)
        glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "Ld"), 1.0, 1.0, 1.0)
        glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "Ls"), 1.0, 1.0, 1.0)

        glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "Ka"), 1.0, 1.0, 1.0)
        glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "Kd"), 1.0, 1.0, 1.0)
        glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "Ks"), 1.0, 1.0, 1.0)


        # TO DO: Explore different parameter combinations to understand their effect!

        glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "lightPosition"), car.x, car.y, car.z + 8)
        glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "viewPosition"), viewPos[0], viewPos[1], viewPos[2])
        glUniform1ui(glGetUniformLocation(lightingPipeline.shaderProgram, "shininess"), 100)

        glUniform1f(glGetUniformLocation(lightingPipeline.shaderProgram, "constantAttenuation"), 0.0001)
        glUniform1f(glGetUniformLocation(lightingPipeline.shaderProgram, "linearAttenuation"), 0.09)
        glUniform1f(glGetUniformLocation(lightingPipeline.shaderProgram, "quadraticAttenuation"), 0.09)

        glUniformMatrix4fv(glGetUniformLocation(lightingPipeline.shaderProgram, "view"), 1, GL_TRUE, view)
        glUniformMatrix4fv(glGetUniformLocation(lightingPipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)

        car.update(controller.r, controller.theta)
        box.update()
        sun.update()
        sg.drawSceneGraphNode(car.node,lightingPipeline,"model")
        sg.drawSceneGraphNode(track.node,lightingPipeline,"model")
        sg.drawSceneGraphNode(sky.node,lightingPipeline,"model")
        sg.drawSceneGraphNode(box.node,lightingPipeline,"model")
        sg.drawSceneGraphNode(sun.node,lightingPipeline,"model")


        # Once the drawing is rendered, buffers are swap so an uncomplete drawing is never seen.
        glfw.swap_buffers(window)

    glfw.terminate()
