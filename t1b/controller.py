import glfw
import sys

# A class to store the application control
class Controller:
    def __init__(self):
        #Movimiento en el eje x
        self.dx = 0
        #Movimiento en el eje y
        self.dy = 0
        #Disparo bala
        self.shot = False


    def mod(self):
        if controller.dx < -1:
            controller.dx = 1
        if controller.dx > 1: 
            controller.dx = -1
        if controller.dy > 1.8:
            controller.dy = 1.8
        if controller.dy < 0:
            controller.dy = 0
        controller.shot = False

# global controller as communication with the callback function
controller = Controller()

def on_key(window, key, scancode, action, mods):
    if action != glfw.PRESS:
        return

    global controller

    #Al apretar la tecla W, la nave se mueve hacia arriba en el espacio 
    if key == glfw.KEY_W:
        controller.dy += 0.1

    #Al apretar la tecla S, la nave se mueve hacia abajo en el espacio 
    elif key == glfw.KEY_S:
        controller.dy += -0.1

    #Al apretar la tecla D, la nave se mueve hacia la derecha
    elif key == glfw.KEY_D:
        controller.dx += 0.1

    #Al apretar la tecla A, la nave se mueve hacia la izquierda
    elif key == glfw.KEY_A:
        controller.dx += -0.1
    #Al apretar la tecla SPACE, la nave dispara
    elif key == glfw.KEY_SPACE:
        controller.shot = True


    #Al apretar la tecla ESCAPE, se cierra la ventana y termina el programa
    elif key == glfw.KEY_ESCAPE:
        sys.exit()

    else:
        print("Unknown key")



