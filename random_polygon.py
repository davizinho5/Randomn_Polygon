# python version

import math
import random

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.tri as mtri

from scipy.spatial import Delaunay
from scipy.spatial import ConvexHull

from copy import deepcopy

### VECTORES ###
def length(v):
  return math.sqrt(dotproduct(v, v))

def dotproduct(v1, v2):
  return sum((a*b) for a, b in zip(v1, v2))
### VECTORES ###  
  
DEBUG = 0
  
def simple_polygon(numVert):
    if numVert < 3:
        x = []
        y = []
        dt = []
        print 'No se puede hacer un poligono de menos de 3 vertices'
        return [x, y, dt]

    # Create an array of random points
    points = []
    for i in range(0, int(numVert)):
        x = random.random()
        y = random.random()
        points.append([x, y])        
       
    points = np.array(points)

    tri = Delaunay(points)    
    hull = ConvexHull(points)   
    
    # Order the edges of the convex hull
    simplices = []
    simplices = deepcopy(hull.simplices)
    for i in range(1, len(hull.simplices)):
        edge_ant = simplices[i-1]
        for j in range(0, len(hull.simplices)):
            edge = hull.simplices[j]
            if ( (edge_ant[1] == edge[0]) and (edge_ant[0] != edge[1]) ):          
                simplices[i] = [edge_ant[1], edge[1]]
                break
            elif( (edge_ant[1] == edge[1]) and (edge_ant[0] != edge[0]) ):
                simplices[i] = [edge_ant[1], edge[0]]
                break
                
    hull.simplices = simplices          
       
    # Plot resulting triangulation, not really necessary
    plt.triplot(points[:,0], points[:,1], tri.simplices)
    plt.plot(points[:,0], points[:,1], 'o')
    for simplex in hull.simplices:
        plt.plot(points[simplex, 0], points[simplex, 1], 'k-')  
    plt.show()
    
    # Look for points that are not part of the convex hull
    idx = []  
    for i in range(0, len(points)):
        pt = [points[i, 0], points[i, 1]]
        equal = []
        for vert in hull.vertices:
            equal.append( (pt[0] == hull.points[vert,0]) and (pt[1] == hull.points[vert,1]) )

        if sum(equal) == 0:
            dist_to_edge = []
            for edge in hull.simplices:
                # distance to each edge of the convex hull
                A = hull.points[edge[0]]            
                B = hull.points[edge[1]]            
                vec1 = [A[0] - B[0], A[1] - B[1]]
                vec2 = [A[0] - pt[0], A[1] - pt[1]]
                dist_to_edge.append(length([np.cross(vec1, vec2),0])/length(vec1))
                
            # save the index of the point to introduce and the edge to break
            idx.append([i, dist_to_edge.index(min(dist_to_edge))])

    if DEBUG:
        print idx

    poligono = []         
    # Create a new polygon which includes all the points 
    if len(idx) == 0:
        print 'No se toca el poligono'
        for vert in hull.vertices:        
            poligono.append(hull.points[vert])
                       
    else:
        poligono.append(hull.points[hull.simplices[0,0]])
        if DEBUG:        
            print hull.simplices
            
        for i in range(0, len(hull.simplices)):
            break_this_edge = []
            dist = []
            
            for change in idx:
                break_this_edge.append(i == change[1])
                if (break_this_edge[-1]):
                    if DEBUG:
                        print 'Break edge', i, 'with point', change[0]
                    dist.append(length(hull.points[hull.simplices[i,0]]-points[change[0]]))
                else:
                    # this number is higher than the maximum possible distance
                    dist.append(10)
            if DEBUG:                
                print 'SUM', sum(break_this_edge)     
                print 'punto_def', hull.simplices[i,0]                                

            poligono.append(hull.points[hull.simplices[i,0]])        
            if sum(break_this_edge) == 1:
                j = break_this_edge.index(True)
                pt_idx =  idx[j]
                if DEBUG:
                    print 'idx', idx
                    print 'punto_sum1', pt_idx[0]

                poligono.append(points[pt_idx[0]])
            elif sum(break_this_edge) > 1:
                if DEBUG:
                    print idx
                for k in range(0,sum(break_this_edge)):
                    idx_unir = idx[dist.index(min(dist))]
                    if DEBUG:
                        print 'punto_sum2', idx_unir[0]
                    poligono.append(points[idx_unir[0]])
                    dist[dist.index(min(dist))] = 10

    if DEBUG:
        print 'poligono', poligono       
        
    plt.plot(points[:,0], points[:,1], 'o')
    x=[]
    y=[]
    for pt in poligono:
        x.append(pt[0])
        y.append(pt[1])
    pt = poligono[0]
    x.append(pt[0])
    y.append(pt[1])        
    plt.plot(x, y, 'r-')  
    plt.show()

if __name__ == "__main__":
    simple_polygon(8)
    
    
