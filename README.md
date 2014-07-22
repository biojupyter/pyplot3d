PyPlot3D
========

This is a package to create rotatable three dimensional graphs in a
ipython notebook. It does so by writing a temporary file with html,
and including that in the notebook. It uses three.js to do so.

The project is currently in the planning stage, but has the following
goals:

1. Create the following graphics objects
    1. Point
    2. Line
    3. Triangle
    4. Polygon
    5. Circle
    6. Cylinder
    7. Sphere
2. Implement a write function for each object that creates a
   corresponding three.js object.
    1. Implement a default point style, line style, and materials.
    2. Implement methods to set point style, line style, and
       materials.
3. Implement the surrounding boiler plate.
    1. Find center of frame based on weighted average of all objects
       in the plot (weight the objects based on surface area).
    2. Find camera viewing angle based on standard deviation of the
       surface area of all objects.
    3. Include camera rotation based on dragging the mouse.
    4. Define default lighting.
    4. Includes methods to set starting camera position, camera
       vertical vector, camera viewing angle, and lighting.
4. Implement wrapper functions for a few simplified 3-D plots
    1. scatter plot
    2. line plot
    3. surface plot (both array data, and mesh data)

The ultimate goal is to make rotatable 3-D plots easy to create and
use in ipython.