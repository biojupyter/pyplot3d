# Vector3 is a list of 3 floats

# Edge is a list of 2 integers (indices)

# Face is a list of 3 integers (indices)

# Mesh is a list of Vector3s, a list of Edges, and a list of Faces

# Line is a mesh with two Vector3s and an Edge

# Triangle is a mesh with three Vector3s, three Edges, and a Face

# Polygon is a list of Coplanar Vector3s, a list of Edges the define
# the perimeter, a list of Faces the define the interior

# A Sphere is a single Vector3 and a float

# A Cylinder is two Vector3s (centers of the circular caps), and a
# radius.

import copy
import math

class Vector3:
  __slots__ = ('_v',)

  def __init__(self, *args):
    if not args:
      self._v = [0., 0., 0.]
    elif len(args) == 1:
      if isinstance( args[0], Vector3):
        self._v = copy.copy(args[0]._v)
      else:
        self._v = [float(x) for x in args[0][:3]]
    elif len(args) == 3:
      self._v = [float(x) for x in args[:3]]
    else:
      raise ValueError("Vector3.__init__ takes 0, 1, or 3 parameters")

  def __str__(self):
    return "{},{},{}".format(self._v[0],self._v[1],self._v[2])

  def __add__(self, other):
    if isinstance(other, Vector3):
      return Vector3([x+y for x,y in zip(self._v,other._v)])
    else:
      return Vector3([x+float(other) for x in self._v])

  __radd__ = __add__

  def __mul__(self, other):
    if isinstance(other, Vector3):
      return sum([x*y for x,y in zip(self._v,other._v)])
    else:
      return Vector3([x*float(other) for x in self._v])

  __rmul__ = __mul__

  def mag(self):
    return math.sqrt(sum([x*x for x in self._v]))

  def norm(self):
    scale = 1./self.mag()
    return Vector3([x*scale for x in self._v])

  def normalize(self):
    scale = 1./self.mag()
    self._v = [x*scale for x in self._v]

  def newTHREE(self, *args):
    return (" "*args[0])+"new THREE.Vector3({})".format(self)

class Edge:
  __slots__ = ('_v',)

  def __init__(self, *args):
    if len(args) == 1:
      if isinstance( args[0], Edge):
        self._v = copy.copy(args[0]._v)
      else:
        self._v = [int(x) for x in args[0][:2]]
    elif len(args) == 2:
      self._v = [int(x) for x in args[:2]]
    else:
      raise ValueError("Edge.__init__ takes 1 or 2 parameters")

class Face:
  __slots__ = ('_v',)

  def __init__(self, *args):
    if len(args) == 1:
      if isinstance( args[0], Face):
        self._v = copy.copy(args[0]._v)
      else:
        self._v = [int(x) for x in args[0][:3]]
    elif len(args) == 3:
      self._v = [int(x) for x in args[:3]]
    else:
      raise ValueError("Face.__init__ takes 1 or 3 parameters")

class Mesh:
  __slots__ = ('_v','_p','_e','_f',)

  def __init__(self, *args):
    if len(args) == 1:
      if isinistance( args[0], Mesh):
        self._v = copy.copy(args[0]._v);
        self._p = copy.copy(args[0]._p);
        self._e = copy.copy(args[0]._e);
        self._f = copy.copy(args[0]._f);
      else:
        self._v = [Vector3(x) for x in args[0][0]]
        self._p = [int(x) for x in args[0][1]]
        self._e = [Edge(x) for x in args[0][2]]
        self._f = [Face(x) for x in args[0][3]]
    elif len(args) == 4:
      self._v = [Vector3(x) for x in args[0]]
      self._p = [int(x) for x in args[1]]
      self._e = [Edge(x) for x in args[2]]
      self._f = [Face(x) for x in args[3]]
    else:
      raise ValueError("Mesh.__init__ takes 1 or 4 parameters")

  def toTHREEjs(self):
    if len(self._p):
      mat_string = """\
      var material = new THREE.PointCloudMaterial({
        color = 0x000000,
        size = 1.0,
        sizeAttenuation = false,
        vertexColors = false,
      });
      """
      geo_string = """\
      var geometry = new THREE.Geometry();
      geometry.vertices.push(
        {}
      )
      """
      verts = [self._v[i] for i in self._p];
      vert_strs = ["new THREE.Vector3({})".format(x._v) for x in verts]
      allverts_str = ",/n".join(vert_strs)
      mat_string+geo_string

_p_mat_str = """\
var material = new THREE.PointCloudMaterial({{
  color : {},
  size : {},
  sizeAttenuation : false,
  fog : true
}})
"""

_p_color = '0x000000'
_p_size = 1.0

_p_geo_str = """\
var geometry = new THREE.Geometry();
geometry.vertices.push(
  {}
)
"""

_p_add_str = """\
var mesh = new THREE.Mesh( geometry, material);
scene.add( mesh);
"""

_l_mat_str = """\
var material = new THREE.LineBasicMaterial({{
  color : {},
  linewidth : {},
  fog : true
}})
"""

_l_color = '0x000000'
_l_linewidth = 1

_l_geo_str = _p_geo_str

_l_add_str = _p_add_str

_m_mat_str = """\
var material = new THREE.MeshPhongMaterial( {{
  color : {},
  ambient : {},
  specular : {},
  emissive : {},
  shininess : {},
  transparent : {},
  opacity : {},
  wireframe : false,
  fog : true,
}});
"""
_m_color = "0xcccccc"
_m_ambient = "0xffffff"
_m_emisive = "0x000000"
_m_specular = "0x444444"
_m_shininess = 100
_m_transparent = "false"
_m_opacity = 1.0
