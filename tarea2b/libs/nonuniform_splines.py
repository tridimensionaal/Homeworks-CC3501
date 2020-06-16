import numpy as np
import matplotlib.pyplot as plt

def generateT(t):
    return np.array([t**3,t**2,t,1])

def hermiteMatrix(P1, P2, T1, T2):
    # Generate a matrix concatenating the columns
    G = np.array([P1,P2,T1,T2])
    # Hermite base matrix is a constant
    Mh = np.array([[2,-2,1,1], [-3,3,-2,-1], [0,0,1,0], [1,0,0,0]])    
    
    return np.matmul(Mh,G)

def getPostionCubic(p1,t1,p2,t2,t):
    ts = generateT(t)
    H = hermiteMatrix(p1,p2,t1,t2)
    return np.matmul(ts,H)

class Node:
    def __init__(self, position):
        self.position = np.array(position)
        self.velocity = 0
        self.distance = 0
        self.steps = 0
        self.list = 0

class Nodes:
    def __init__(self,nodes):
        n = len(nodes)
        s = np.array([14,8,10,10,8,14,14,8,10,10,8,14])
        s *= 4

        for i in range(n):
            nodes[i].steps = s[i]

        for i in range(n):
            if i == 0:
                velocity = (nodes[1].position - nodes[n-1].position)/2
            elif i == n-1:
                velocity = (nodes[0].position - nodes[n-2].position)/2
            else:
                velocity = (nodes[i+1].position - nodes[i-1].position)/2
            #velocity = velocity/np.linalg.norm(velocity)

            nodes[i].velocity = velocity

        for i in range(n):
            node = nodes[i]
            nodesig = nodes[(i+1)%n]
            steps = node.steps
            l = []

            p1 = node.position
            p2 = nodesig.position
            t1 = node.velocity
            t2 = nodesig.velocity

            for j in range(steps):
                t = j/steps
                p = getPostionCubic(p1,t1,p2,t2,t)
                l += [p]

            nodes[i].list = np.array(l)

        self.nodes = nodes
'''
p0 = np.array([8,0,0])
p1 = np.array([5,6,0])
p2 = np.array([3,3,0])
p3 = np.array([0,7,0.1])
p4 = np.array([-3,3,0.1])
p5 = np.array([-5,6,0])
p6 = np.array([-8,0,0.5])
p7 = np.array([-5,-6,0.5])
p8 = np.array([-3,-3,0.5])
p9 = np.array([0,-7,0])
p10 = np.array([3,-3,0])
p11 = np.array([5,-6,0])

points1 = np.array([p0,p1,p2,p3,p4,p5,p6,p7,p8,p9,p10,p11])
points1 *= 50

nodes = np.ndarray((12),dtype=Node)
for i in range(len(points1)):
    point = points1[i]
    node = Node(point)
    nodes[i] = node

nodes1 = Nodes(nodes)

p0 = np.array([7,0,0])
p1 = np.array([5,4,0])
p2 = np.array([3,1,0])
p3 = np.array([0,5,0.1])
p4 = np.array([-3,1,0.1])
p5 = np.array([-5,4,0])
p6 = np.array([-7,0,0.5])
p7 = np.array([-5,-4,0.5])
p8 = np.array([-3,-1,0.5])
p9 = np.array([0,-5,0])
p10 = np.array([3,-1,0])
p11 = np.array([5,-4,0])

points2= np.array([p0,p1,p2,p3,p4,p5,p6,p7,p8,p9,p10,p11])
points2 *= 50

nodes = np.ndarray((12),dtype=Node)

for i in range(len(points2)):
    point = points2[i]
    node = Node(point)
    nodes[i] = node

nodes2 = Nodes(nodes)

points1 =[]
points2 = []
x1 = []
y1 = []
x2 = []
y2 = []

for node in nodes1.nodes:
    for point in node.list:
        points1 += [point]
        x1 += [point[0]]
        y1 += [point[1]]
        y1 += [point[2]]

for node in nodes2.nodes:
    for point in node.list:
        points2 += [point]
        x2 += [point[0]]
        y2 += [point[1]]
        z2 += [point[2]]

plt.plot(x1,y1,'ro')
plt.plot(x2,y2,'ro')
plt.show()
'''
