import numpy as np
import matplotlib.pyplot as plt

#Función que retorna un vector tiempo
def generateT(t):
    return np.array([t**3,t**2,t,1])

#Función que retorna un vector de la derivada del tiempo
def generateDT(t):
    return np.array([3*t**2,2*t,1,0])


#Función que dado que dos puntos p1,p2 y dos tangentes t1, t2, retorna el producto matricial entre la matriz geometría (G) y la matriz de hermite (Mh).
def hermiteMatrix(P1, P2, T1, T2):
    G = np.array([P1,P2,T1,T2])
    Mh = np.array([[2,-2,1,1], [-3,3,-2,-1], [0,0,1,0], [1,0,0,0]])    
    return np.matmul(Mh,G)

#Función que dado dos puntos (p1 y p2) y sus velocidades (t1 y t2), se calcula un punto intermedio entre p1 y p2 dado un tiempo t e [0,1]
def getPositionCubic(p1,t1,p2,t2,t):
    ts = generateT(t)
    H = hermiteMatrix(p1,p2,t1,t2)
    return np.matmul(ts,H)

#dado dos puntos (p1 y p2) y sus velocidades (t1 y t2), se calcula la velocidad de un punto intermedio entre p1 y p2 dado un tiempo t e [0,1]
def getTanCubic(p1,t1,p2,t2,t):
    ts = generateDT(t)
    H = hermiteMatrix(p1,p2,t1,t2)
    return np.matmul(ts,H)


#Clase que almacena la información asociada a un punto (nodo)
class Node:
    def __init__(self, position):
        self.position = np.array(position)
        self.velocity = 0
        self.distance = 0
        self.totalDistance = 0

#Clase que, dado un conjunto de puntos (nodo), se crea una nonuniform spline dado el conjunto.
class Nodes:
    def __init__(self,nodes,steps):
        n = len(nodes)
        maxDistance = 0

        for i in range(n):
            nodes[i].distance = np.linalg.norm(nodes[(i+1)%n].position - nodes[i].position)
            maxDistance += nodes[i].distance
            nodes[i].totalDistance = maxDistance

        for i in range(n):
            if i == 0:
                x = nodes[n-1].position- nodes[0].position
                y = nodes[1].position- nodes[0].position
            elif i == n-1:
                x = nodes[n-2].position- nodes[n-1].position
                y = nodes[0].position- nodes[n-1].position
            else:
                x = nodes[i-1].position- nodes[i].position
                y = nodes[i+1].position- nodes[i].position

            x = x/np.linalg.norm(x)
            y = y/np.linalg.norm(y)

            velocity = (y-x)
            nodes[i].velocity = velocity


        s = maxDistance/steps
        j = 0
        points = []
        tans = []

        for i in range(steps+1):
            distance = i*s

            while distance > nodes[j].totalDistance:
                j += 1

            if j == 0:
                t = distance
            else:
                t = distance - nodes[j-1].totalDistance

            t /= nodes[j].distance

            p1 = nodes[j].position
            p2 = nodes[(j+1)%n].position
            t1 = nodes[j].velocity*nodes[j].distance
            t2 = nodes[(j+1)%n].velocity*nodes[j].distance

            p = getPositionCubic(p1,t1,p2,t2,t)
            points += [p]

            tan = getTanCubic(p1,t1,p2,t2,t)
            tan = tan/np.linalg.norm(tan)
            tans += [tan]

        #Se almacena los puntos de la nonuniform spline
        self.points = np.array(points)
        #Se almacena las velocidades de los puntos de la nonuniform spline
        self.tans = np.array(tans)

#Función que dada un conjunto de puntos, una cantidad de puntos y un valor constante, retorna una pista generada a través de una nonuniform spline
class Track:
    def __init__(self,points,steps,n):
        points *= n
        large = len(points)

        l = np.ndarray((large),dtype=Node)

        for i in range(large):
            point = points[i]
            node = Node(point)
            l[i] = node

        nodes = Nodes(l,steps)

        points = []
        large = len(nodes.points)

        for i in range(large):
            tx = nodes.tans[i][0]
            ty = nodes.tans[i][1]
            tz = nodes.tans[i][2]

            nor = np.array([ty,-tx,tz])

            p = nodes.points[i] - (n/2)*nor
            px = p[0]
            py = 0.9*p[1]
            pz = p[2]

            p = np.array([px,py,pz])
            points += [p]

        points = np.array(points)

        self.ext = nodes.points
        self.int = points


'''
p0 = np.array([8,0,0])
p1 = np.array([5,6,0])
p2 = np.array([3,3,0])
p3 = np.array([0,7,0])
p4 = np.array([-3,3,0])
p5 = np.array([-5,6,0])
p6 = np.array([-8,0,0])
p7 = np.array([-5,-6,0])
p8 = np.array([-3,-3,0])
p9 = np.array([0,-7,0])
p10 = np.array([3,-3,0])
p11 = np.array([5,-6,0])

points = np.array([p0,p1,p2,p3,p4,p5,p6,p7,p8,p9,p10,p11])


track = Track(points,300,100)

x1 = []
y1 = []
x2 = []
y2 = []


n = len(track.ext)

for i in range(n):
    x1 += [track.ext[i][0]]
    y1 += [track.ext[i][1]]

    x2 += [track.int[i][0]]
    y2 += [track.int[i][1]]


plt.plot(x1,y1,'ro')
plt.plot(x2,y2,'ro')
plt.show()
'''
