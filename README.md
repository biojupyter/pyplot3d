I want to make a 2-D and 3-D rendering library which uses THREE.js to
render into a web page. Specifically, I am targeting manipulatable
3-D graphs that can be created in a iPython notebook.

Math types: These types support the math necessary for 2-D and 3-D
rendering
- Vector2D : A two dimensional vector.
- Matrix3 : A 3x3 matrix for transforming the 2-D vector.
- *Vector3D* : A three dimensional vector.
- Matrix4 : A 4x4 matrix for transforming the 3-D vector.

Geometry types : These types hold the geometry information
*GeoObj* : This is the base class.
- Sprite : A 2-D picture rendered at a vertex.
      + PointSet : A collection of points (vertices) that will render
        as fixed sized point.
      + Text : Text that renders at a vertex.
- *Line* : A single connected line between many vertices.
- *TriangleSet* : A set of triangles drawn between vertices.
- *GeoSet* : A collection of sprites, lines, triangles that all share
  the same set of indexed vertices.
    + Polygon : A geoset with a line around the perimeter, and
      triangles in the center.
        * Rectangle
    + Box : A geoset that describes a box. It has lines at the edges,
      and triangles filling in the faces.
    + Frame2D : A GeoSet that describes frame with tickmarks and
      text.
    + Frame3D : A GeoSet that has a box outline with tickmarks, the
      rear faces of the mesh should have a wiremesh in addition to
      the tickmarks on the box outlines.

Functions : These are the functions to define
- Render2D : This function takes a list of 2-D GeoObj and renders
  them onto a canvas using THREE.js
- *Render3D* : This function takes a list of 3-D GeoObj and renders
  then onto a canvas using THREE.js