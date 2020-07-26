import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import sys
import json


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

    if not glfw.init():
        sys.exit()

    #Tamaño de la ventana
    #Ventana
    window = glfw.create_window(width, height, "Aquarium View", None, None)

    if not window:
        glfw.terminate()
        sys.exit()

    glfw.make_context_current(window)

    #Se conecta la ventana con la función on_key
    glfw.set_key_callback(window, on_key)

    #Color de fondo de la ventana
    glClearColor(0.7, 0.7, 0.7, 1.0)

    #Se activan las transparencia
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    glEnable(GL_DEPTH_TEST)

    return window


if __name__ == "__main__":
    name = sys.argv[1]
    name = "./" + str(name)

    with open(name) as f:
        data = json.load(f)


    filename = "./" + data["filename"]

    aquarium = np.load(filename)

    window = windowConf()

    #Se inicializa el shader program
    lightingPipeline = light_s.SimpleTextureGouraudShaderProgram(0.1)
    lightingPipeline2 = light_s.SimpleTextureGouraudShaderProgram(1)

    #Se crean las shapes 
    scene = model.Scene(data,aquarium)
    x = scene.aquarium.x
    y = scene.aquarium.y
    z = scene.aquarium.z

    controller.camera().updateAt(x/2,y/2, z/2)
    controller.set_r(x,y)

    while not glfw.window_should_close(window):
        #Se utiliza GLFW y la función key para checkear inputs del teclado
        glfw.poll_events()
        key2(window)

        # Se inicializa la projección a usar
        projection = tr.perspective(60, float(width)/float(height), 0.1, 2500)

        scene.update(0,0,0)

        #Se actualiza la vista
        controller.camera().updateEye(controller.r,controller.theta)
        view = controller.camera().update_view()
        viewPos = controller.camera().view_pos()

        #Se limpia la pantalla
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glUseProgram(lightingPipeline2.shaderProgram)

        #Componentes de la luz: ambiente, difuso y especular
        glUniform3f(glGetUniformLocation(lightingPipeline2.shaderProgram, "La"), 0.7, 0.7, 0.7)
        glUniform3f(glGetUniformLocation(lightingPipeline2.shaderProgram, "Ld"), 1.0, 1.0, 1.0)
        glUniform3f(glGetUniformLocation(lightingPipeline2.shaderProgram, "Ls"), 1.0, 1.0, 1.0)
        
        #Propiedas de los objetos respecto a la luz
        glUniform3f(glGetUniformLocation(lightingPipeline2.shaderProgram, "Ka"), 1.0, 1.0, 1.0)
        glUniform3f(glGetUniformLocation(lightingPipeline2.shaderProgram, "Kd"), 1.0, 1.0, 1.0)
        glUniform3f(glGetUniformLocation(lightingPipeline2.shaderProgram, "Ks"), 1.0, 1.0, 1.0)

        #Se configura la luz
        glUniform3f(glGetUniformLocation(lightingPipeline2.shaderProgram, "lightPosition"), x/2 ,y/2,z/2)
        glUniform3f(glGetUniformLocation(lightingPipeline2.shaderProgram, "viewPosition"), viewPos[0], viewPos[1], viewPos[2])
        glUniform1ui(glGetUniformLocation(lightingPipeline2.shaderProgram, "shininess"), 1000)
        glUniform1f(glGetUniformLocation(lightingPipeline2.shaderProgram, "constantAttenuation"), 0.0001)
        glUniform1f(glGetUniformLocation(lightingPipeline2.shaderProgram, "linearAttenuation"), 0.09)
        glUniform1f(glGetUniformLocation(lightingPipeline2.shaderProgram, "quadraticAttenuation"), 0.09)

 

        glUniformMatrix4fv(glGetUniformLocation(lightingPipeline2.shaderProgram, "view"), 1, GL_TRUE, view)
        glUniformMatrix4fv(glGetUniformLocation(lightingPipeline2.shaderProgram, "projection"), 1, GL_TRUE, projection)
 
        sg.drawSceneGraphNode(scene.fishes.node,lightingPipeline2,"model")

        #Se especifica que shader usar
        glUseProgram(lightingPipeline.shaderProgram)

        #Componentes de la luz: ambiente, difuso y especular
        glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "La"), 0.7, 0.7, 0.7)
        glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "Ld"), 1.0, 1.0, 1.0)
        glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "Ls"), 1.0, 1.0, 1.0)
        
        #Propiedas de los objetos respecto a la luz
        glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "Ka"), 1.0, 1.0, 1.0)
        glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "Kd"), 1.0, 1.0, 1.0)
        glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "Ks"), 1.0, 1.0, 1.0)

        #Se configura la luz
        glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "lightPosition"), x/2 ,y/2,z/2)
        glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "viewPosition"), viewPos[0], viewPos[1], viewPos[2])
        glUniform1ui(glGetUniformLocation(lightingPipeline.shaderProgram, "shininess"), 1000)
        glUniform1f(glGetUniformLocation(lightingPipeline.shaderProgram, "constantAttenuation"), 0.0001)
        glUniform1f(glGetUniformLocation(lightingPipeline.shaderProgram, "linearAttenuation"), 0.09)
        glUniform1f(glGetUniformLocation(lightingPipeline.shaderProgram, "quadraticAttenuation"), 0.09)

        glUniformMatrix4fv(glGetUniformLocation(lightingPipeline.shaderProgram, "view"), 1, GL_TRUE, view)
        glUniformMatrix4fv(glGetUniformLocation(lightingPipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
        sg.drawSceneGraphNode(scene.aquarium.node,lightingPipeline,"model")

        glfw.swap_buffers(window)

    glfw.terminate()
