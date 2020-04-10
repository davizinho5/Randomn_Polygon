# python version

import math
import random

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.tri as mtri

from scipy.spatial import Delaunay
from scipy.spatial import ConvexHull

# busca a cuantos simplices corresponden cada vertices de CH
def check_vertex(edges, simplices):
    result = []
    for edge in edges:
        equal = edge == simplices
        result.append(sum(sum(equal)))            
    return result

# busca a que simplices corresponden cada eje de CH
# devuelve numero de simplice del eje
def check_edge(edge, simplices):
    result = []

    for i in range(0, len(simplices)):
        simplex = simplices[i]          
        pt = edge[0]
        aux0 = pt[0]==simplex[:,0]
        aux1 = pt[1]==simplex[:,1]                
        pt = edge[1]
        aux2 = pt[0]==simplex[:,0]
        aux3 = pt[1]==simplex[:,1]     
        aux4 = False     
        aux5 = False     
        for k in range(0, len(aux0)):
            aux4 = aux4 or (aux0[k] and aux1[k])
            aux5 = aux5 or (aux2[k] and aux3[k])

        if (aux4 and aux5):
            result.append(i)
        
    return result        

def simple_polygon(numSides):
    if numSides < 3:
        x = []
        y = []
        dt = []
        return [x, y, dt]

    # Create an array of points.
    points = [];

    fudge = math.ceil(numSides/10);
    for i in range(0, int(numSides+fudge)):
        x = random.random()
        y = random.random()
        points.append([x, y])        
     
    # Igual
    #points = [[0.9300, 0.6862], [0.3990, 0.8936], [0.0474, 0.0548], [0.3424, 0.3037], [0.7360, 0.0462], [0.7947, 0.1955], [0.5449, 0.7202]]
    # Menor
    #points = [[0.6801, 0.1126], [0.3672, 0.4438], [0.2393, 0.3002], [0.3424, 0.4014], [0.8669, 0.8334], [0.4068, 0.4036]]
    # Mayor
    #points = [[0.0868, 0.4951], [0.4294, 0.7064], [0.2573, 0.2436], [0.2976, 0.7851], [0.4249, 0.0741], [0.1192, 0.3939]]
    
    points = np.array(points)

    tri = Delaunay(points)    
    
    # Plot resulting triangulation, not really necessary
    plt.triplot(points[:,0], points[:,1], tri.simplices)
    plt.plot(points[:,0], points[:,1], 'o')

    hull = ConvexHull(points)    

    plt.plot(points[:,0], points[:,1], 'o')
    for simplex in hull.simplices:
        plt.plot(points[simplex, 0], points[simplex, 1], 'k-')  
    plt.show()
        
    numEdges = len(hull.simplices)
    
    keep = []   
    while numEdges != numSides:
        if numEdges > numSides:
            print 'mayor'        
# busca a cuantos simplices corresponden cada vertices de CH
# recoloca de manera aleatoria, para que?
# para cada vertice, comprueba si corresponde a mas de 1 simplice

            result = np.array(check_vertex(hull.simplices[:,0], tri.simplices))
            keep = (result == 1)
            
        if (numEdges < numSides) or  (sum(keep) == 0): 
            print 'menor'
# busca a que simplices corresponden cada eje de CH
# has only one of its edges on the triangulation boundary
            result = []
            for edge in hull.simplices:
                result.append(check_edge([hull.points[edge[0],:],hull.points[edge[1],:]], tri.points[tri.simplices]))
                 
# recoloca de manera aleatoria, para que?
# simplice de la lista, coge sus puntos
# true para cada miembro de boundaryEdges(:,1)) que aparece en triPoints, en la posicion de triPoints
            triPoints = []
            keep = []
            for idx in result:
                tript = tri.simplices[idx]
                simplex = tript[0]
                temp=[False, False, False]
                for i in range(0,len(simplex)):                   
                    for j in range(0,len(hull.simplices[:,0])):
                        temp[i] = temp[i] or (simplex[i] == hull.simplices[j,0])

                keep.append(temp[0] and temp[1] and temp[2])
                      
        if  (sum(keep) == 0): 
            print 'Could not achieve desired number of sides!'
            break

        # quitar el simplex indicado y volver a triangular  
        new_simplices = []
        for i in range(0,len(keep)):
            if not keep[i]: 
                num = i
                break       
        new_simplices = np.delete(tri.simplices, i,0)
       
        triang = mtri.Triangulation(points[:,0], points[:,1], triangles=new_simplices.tolist())
        hull = ConvexHull(points)   
        numEdges = len(hull.simplices)         
        
    #endwhile
    
    # sacar los puntos del contorno
    boundary = hull.simplices[:,0].tolist()
    boundary.append(hull.simplices[0,0])
    print 'boundary', boundary
       
    points = hull.points[boundary]
    print 'points', points

    plt.plot(points[:,0], points[:,1], 'o')
    for simplex in hull.simplices:
        plt.plot(points[simplex, 0], points[simplex, 1], 'k-')  
    plt.show()


if __name__ == "__main__":
    simple_polygon(4)
    
    
    
    
