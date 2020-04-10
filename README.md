# Random_Polygon

Matlab and Python functions to generate random polygons which can be convex or concave. 


The Python function to create random polygons was created using the one written in Matlab as inspiration. In my opinion, it is easier to understand an implement. It has been tested up to ten vertices, if you find any problem, please write me a comment. The code follows the next step:

1. Genarate an array of random points which will be the vertices if the polygon. The number of vertices is selected by the user, and it must be larger than 2. 

2. Create the convex hull of the points. 

3. Find the points which are not part of the convex hull and compute their distance to the edges of the convex hull. If all of them are part of it, we have finished. 

4. Otherwise, create a new polygon in which these points are introduced in the polygon breaking the closest edge of the convex hull. 

---------------------------------------------------------

The Matlab function is taken from here:

https://stackoverflow.com/questions/8997099/algorithm-to-generate-random-2d-polygon

The only difference with the proposed function is that the deprecated fucntions have been updated.

This solution uses the Matlab built-in function related to traingulations and is not easy to be implemented without them. As explained in stackoverflow, the code follows these steps to create an arbitrary simple polygon:

1. Generate a number of random points equal to the desired number of sides plus a fudge factor. The fudge factor ensures that, regardless of the result of the triangulation, we should have enough facets to be able to trim the triangular mesh down to a polygon with the desired number of sides.

2. Create a Delaunay triangulation of the points, resulting in a convex polygon that is constructed from a series of triangular facets.

3. If the boundary of the triangulation has more edges than desired, pick a random triangular facet on the edge that has a unique vertex (i.e. the triangle only shares one edge with the rest of the triangulation). Removing this triangular facet will reduce the number of boundary edges.

4. If the boundary of the triangulation has fewer edges than desired, or the previous step was unable to find a triangle to remove, pick a random triangular facet on the edge that has only one of its edges on the triangulation boundary. Removing this triangular facet will increase the number of boundary edges.

5. If no triangular facets can be found matching the above criteria, post a warning that a polygon with the desired number of sides couldn't be found and return the x and y coordinates of the current triangulation boundary. Otherwise, keep removing triangular facets until the desired number of edges is met, then return the x and y coordinates of triangulation boundary.

