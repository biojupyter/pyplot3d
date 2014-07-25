# A Vector3 contains 3 floats

class Vector3:
  __slots__ = ('_v',)

  def __init__(self, *args):
    if not args:
      self._v = [0., 0., 0.]
    elif len(args) == 1:
      if isinstance(args[0], Vector3):
        self = args[0].copy
      else
        self._v = map(float, args[0][:3])
    elif len(args) == 3:
      self._v = map(float, args[:3])
    else:
      raise ValueError("Vector3.__init__ takes 0, 1, or 3 args.")

class Edge:
  __slots__ = ('_v',)

  def __init__(self, *args):
    if len(args) == 1:
      if isinstance(args[0], Edge):
        self = args[0].copy
      else
        self._v = map(int, args[0][:2])
    elif len(args) == 3:
      self._v = map(int, args[:2])
    else:
      raise ValueError("Edge.__init__ takes 1 or 2 args.")

class Face:
  __slots__ = ('_v',)

  def __init__(self, *args):
    if len(args) == 1:
      if isinstance(args[0], Face)
        self = args[0].copy
      else
        self._v = map(int, args[0][:3])
    elif len(args) == 3:
      self._v = map(int, args[:3])
    else:
      raise ValueError("Face.__init__ takes 1 or 3 args.")

class Mesh(GoemetryObject):
  def __init__(self, *args):
    if not args:
      self.vertices = []
      self.points = []
      self.edges = []
      self.faces = []
    elif len(args) == 1:
      self.vertices = args[0][0]
      self.points = args[0][1]
      self.edges = args[0][2]
      self.faces = args[0][3]
    elif len(args) == 4:
      self.vertices = args[0]
      self.points = args[1]
      self.edges = args[2]
      self.faces = args[3]
    else:
      raise ValueError("Mesh.__init__ takes 0, 1, or 4 args.")

  def add_vertex(self, *args):
    if len(args) == 3 && not isinstance(args[0], Vector3):
      self.vertices.add( Vector3(*args)) 
    elif args:
      map(lambda x: self.vertices.add(Vector3(x)), args[:])
    else:
      raise ValueError("Mesh.add_vertex must have >0 args.")

  def add_point(self, *args):
    if args:
      map(lambda x: self.points.add(int(x)), args[:])
    else:
      raise ValueError("Mesh.add_vertex must have >0 args.")

  def add_edge(self, *args):
    if len(args) == 2 && not isinstance(args[0], Edge):
      self.edges.add( Edge(*args)) 
    elif args:
      map(lambda x: self.edges.add(Edge(x)), args[:])
    else:
      raise ValueError("Mesh.add_vertex must have >0 args.")

  def add_face(self, *args):
    if len(args) == 3 && not isinstance(args[0], Face):
      self.faces.add( Face(*args)) 
    elif args:
      map(lambda x: self.faces.add(Face(x)), args[:])
    else:
      raise ValueError("Mesh.add_vertex must have >0 args.")

class Point(Mesh):

class Line(Mesh):

class Triangle(Mesh):

class Polygon(Mesh):

class Sphere(GeometryObject):

class Cylinder(GoemetryObject):

class Box(GeometryObject):