import numpy as np
import json
import sys 
from scipy.sparse import lil_matrix
from scipy.sparse.linalg import spsolve

name = sys.argv[1]
name = "./" + str(name)

with open(name) as f:
    data = json.load(f)


#zmax
H = data["height"]
#ymax
W = data["width"]
#xmax
L = data["lenght"]
#
B = data["window_loss"]
#
TA = data["heater_a"]
#
TB = data["heater_b"]
#
Tamb = data["ambient_temperature"]
#
h = 0.25

nW= int(W/h)
nH = int(H/h) 
nL = int(L/h)

N = nH*nW*nL
print(N)

def getP(i,j,k):
    return k*(nW*nL) + j*nL +  i

def getIJK(p):
    i = p%nL
    p -= i
    p //= nL

    j = p%nW
    p -= j

    k = p//nW

    return(i,j,k)

A = lil_matrix((N,N))
b = np.zeros(N)

for i in range(nL):
    for j in range(nW):
        for k in range(nH):
            p = getP(i,j,k)

            px1 = getP(i+1,j,k)
            px2 = getP(i-1,j,k)
            py1 = getP(i,j+1,k)
            py2 = getP(i,j-1,k)
            pz1 = getP(i,j,k+1)
            pz2 = getP(i,j,k-1)

            #Superficie inferior
            if k == 0: 
                #Area calefactor A
                if (i > nL/5 and i < 2*nL/5) and (j > nW/3 and j < 2*nW/3):
                    A[p,p] = 1
                    b[p] = TA
                    continue

                #Area calefactor B
                elif (i > 3*nL/5 and i < 4*nL/5) and (j > nW/3 and j < 2*nW/3):
                    A[p,p] = 1
                    b[p] = TB
                    continue

                #Condición de neumann nula en z
                else:
                    A[p,pz1] = 2

            #Superficie superior, condición de dirichlet
            elif k == nH -1:
                A[p,p] = 1
                b[p] = Tamb
                continue
            #k en el interior del dominio
            else:
                A[p,pz1] = 1
                A[p,pz2] = 1

            #Condición de neumann en x 
            if i == 0:
                A[p,px1] = 2
            #Condición de neumann en x
            elif i == nL-1:
                A[p,px2] = 2
            else:
                A[p,px1] = 1
                A[p,px2] = 1

            #Condición de neumann en y
            if j == 0:
                A[p,py1] = 2

            #Condición de neumann en y
            elif j == nW-1:
                A[p,py2] = 2
            #y en el interior
            else:
                A[p,py1] = 1
                A[p,py2] = 1

            if i==0 and j== 0:
                b[p] = 4*h*B
            elif i == nL-1 and j == nW-1:
                b[p] = -4*h*B
            else:
                b[p] = 0

            A[p,p] = -6

A = A.tocsr()
x = spsolve(A,b)
aquarium = np.zeros((nL,nW,nH))
for p in range(0,N):
    i,j,k = getIJK(p)
    aquarium[i][j][k] = x[p]

np.save(data["filename"],aquarium)

xu = []
yu = []
zu = []
cu = []

for p in range(0, N):
    i,j,k  = getIJK(p)
    cu += [x[p]]
    xu += [i]
    yu += [j]
    zu += [k]

from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt

fig = plt.figure()
ax = plt.axes(projection='3d')
ax.scatter(xu, yu, zu, c=cu, cmap='viridis', linewidth=0.5);
plt.show()

