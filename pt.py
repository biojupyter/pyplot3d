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
from uuid import uuid4 as uuid

class Vector3:

  def __init__(self, *args):
    if not args:
      self.v = [0., 0., 0.]
    elif len(args) == 1:
      if isinstance( args[0], Vector3):
        for attr in args[0].__dict__:
          setattr(self, attr, copy.deepcopy(getattr(args[0],attr)))
      else:
        self.v = [float(x) for x in args[0][:3]]
    elif len(args) == 3:
      self.v = [float(x) for x in args[:3]]
    else:
      raise ValueError("Vector3.__init__ takes 0, 1, or 3 parameters")

  def __iter__(self):
    return iter(self.v[:])

  def __str__(self):
    return "{},{},{}".format(self.v[0],self.v[1],self.v[2])

  def __add__(self, other):
    if isinstance(other, Vector3):
      return Vector3([x+y for x,y in zip(self.v,other.v)])
    else:
      return Vector3([x+float(other) for x in self.v])

  __radd__ = __add__

  def __sub__(self, other):
    if isinstance(other, Vector3):
      return Vector3([x-y for x,y in zip(self.v,other.v)])
    else:
      return Vector3([x-float(other) for x in self.v])

  __rsub__ = __sub__

  def __neg__(self):
    return Vector3([-x for x in self.v])

  def __mul__(self, other):
    if isinstance(other, Vector3):
      return sum([x*y for x,y in zip(self.v,other.v)])
    else:
      return Vector3([x*float(other) for x in self.v])

  __rmul__ = __mul__

  def __truediv__(self, other):
    return Vector3([x/float(other) for x in self.v])

  def cross(self, other):
    x = self.v[1]*other.v[2]-self.v[2]*other.v[1]
    y = self.v[2]*other.v[0]-self.v[0]*other.v[2]
    z = self.v[0]*other.v[1]-self.v[1]*other.v[0]
    return Vector3(x,y,z)

  def mag(self):
    return math.sqrt(sum([x*x for x in self.v]))

  def norm(self):
    scale = 1./self.mag()
    return Vector3([x*scale for x in self.v])

  def transform(self, trans):
    v = self.v.append(1.)
    x = sum([te*ve for ve, te in zip()])

  def THREEjs(self):
    return ("new THREE.Vector3({})".format(self))

class Edge:

  def __init__(self, *args):
    if len(args) == 1:
      if isinstance( args[0], Edge):
        for attr in args[0].__dict__:
          setattr(self, attr, copy.deepcopy(getattr(args[0],attr)))
      else:
        self.v = [int(x) for x in args[0][:2]]
    elif len(args) == 2:
      self.v = [int(x) for x in args[:2]]
    else:
      raise ValueError("Edge.__init__ takes 1 or 2 parameters")

  def __iter__(self):
    return iter(self.v[:])


class Face:

  def __init__(self, *args):
    if len(args) == 1:
      if isinstance( args[0], Face):
        for attr in args[0].__dict__:
          setattr(self, attr, copy.deepcopy(getattr(args[0],attr)))
      else:
        self.v = [int(x) for x in args[0][:3]]
    elif len(args) == 3:
      self.v = [int(x) for x in args[:3]]
    else:
      raise ValueError("Face.__init__ takes 1 or 3 parameters")

  def __iter__(self):
    return iter(self.v[:])

  def __str__(self):
    return "{},{},{}".format(self.v[0],self.v[1],self.v[2])

  def THREEjs(self):
    return ("new THREE.Face3({})".format(self))

class Mesh:

  def __init__(self, *args, **kwargs):
    self.pointColor = _pointColor
    self.pointSize = _pointSize
    self.lineColor = _lineColor
    self.lineWidth = _lineWidth
    self.color = _color 
    self.ambient = _ambient
    self.emisive = _emisive
    self.specular = _specular
    self.shininess = _shininess
    self.transparent = _transparent
    self.opacity = _opacity
    self.smooth = _smooth
    if len(args) == 1:
      if isinstance( args[0], Mesh):
        for attr in args[0].__dict__:
          setattr(self, attr, copy.deepcopy(getattr(args[0],attr)))
      else:
        self.vertices = [Vector3(x) for x in args[0][0]]
        self.points = [int(x) for x in args[0][1]]
        self.edges = [Edge(x) for x in args[0][2]]
        self.faces = [Face(x) for x in args[0][3]]
    elif len(args) == 4:
      self.vertices = [Vector3(x) for x in args[0]]
      self.points = [int(x) for x in args[1]]
      self.edges = [Edge(x) for x in args[2]]
      self.faces = [Face(x) for x in args[3]]
    else:
      raise ValueError("Mesh.__init__ takes 1 or 4 parameters")
    for attr in kwargs:
      if attr in self.__dict__:
        setattr(self, attr, kwargs[attr])

  def boundingBox(self):
    x = [vert.v[0] for vert in self.vertices]
    y = [vert.v[1] for vert in self.vertices]
    z = [vert.v[2] for vert in self.vertices]
    vmin = Vector3( min(x), min(y), min(z))
    vmax = Vector3( max(x), max(y), min(z))
    return (vmin, vmax)

  def pointStats(self):
    points = [self.vertices[i] for i in self.points]
    return (sum(points), len(points))

  def lineCenter(self, line):
    v0, v1 = [self.vertices[i] for i in line]
    return 0.5*(v0+v1)

  def lineLength(self, line):
    v0, v1 = [self.vertices[i] for i in line]
    return (v0-v1).mag()

  def lineStats(self):
    lineCenters = [self.lineCenter(line) for line in self.edges]
    lineLengths = [self.lineLength(line) for line in self.edges]
    num = sum([x*y for x, y in zip(lineCenters, lineLengths)])
    denom = sum(lineLengths)
    return (num, denom)

  def faceCenter(self, face):
    v0, v1, v2 = [self.vertices[i] for i in face]
    return 1./3.*(v0+v1+v2)

  def faceArea(self, face):
    v0, v1, v2 = [self.vertices[i] for i in face]
    e1 = v1-v0
    e2 = v2-v0
    return 0.5*(e1.cross(e2).mag())

  def faceStats(self):
    faceCenters = [self.faceCenter(face) for face in self.faces]
    faceAreas = [self.faceArea(face) for face in self.faces]
    num = sum([x*y for x, y in zip(faceCenters, faceAreas)])
    denom = sum(faceAreas)
    return (num, denom)

  def meshStats(self):
    vmin, vmax = self.boundingBox()
    dw = 0.05*(vmax-vmin).mag()
    pnum, pdenom = self.pointStats()
    lnum, ldenom = self.lineStats()
    fnum, fdenom = self.faceStats()
    num = dw*dw*pnum + dw*lnum + fnum
    denom = dw*dw*pdenom + dw*ldenom + fdenom
    return (num, denom)

  def cameraDistance(self):
    vmin, vmax = self.boundingBox()
    dist = (vmax-vmin).mag()
    return 1.5*0.5*dist/math.sin(45/2*math.pi/180)

  def toTHREEjs(self):
    three_str = ""
    if len(self.points) > 0 :
      vert_str = [ self.v[i].THREEjs() for i in self.points]
      vert_str = ",\n  ".join( vert_str )
      three_str += _p_mat_str.format( self.pointColor, self.pointSize )
      three_str += _p_geo_str.format( vert_str )
      three_str += _p_add_str
    if len(self.edges) > 0 :
      for line in self.edges:
        vert_str = [ self.v[i].THREEjs() for i in line ]
        vert_str = ",\n  ".join( vert_str )
        three_str += _l_mat_str.format( self.lineColor, self.lineWidth )
        three_str += _l_geo_str.format( vert_str )
        three_str += _l_add_str
    vert_str = [ x.THREEjs() for x in self.v ]
    vert_str = ",\n  ".join( vert_str )
    face_str = [ x.THREEjs() for x in self.faces ]
    face_str = ",\n  ".join( face_str )
    three_str += _m_mat_str.format(
      self.color, 
      self.ambient, 
      self.specular, 
      self.emisive, 
      self.shininess, 
      self.transparent, 
      self.opacity
    )
    three_str += _m_geo_str.format( vert_str, face_str )
    if self.smooth :
      three_str += _m_smooth_str
    three_str += _m_add_str
    return three_str

_pointColor = '0x000000'
_pointSize = 4.0
_lineColor = '0x000000'
_lineWidth = 2.
_color = "0xcccccc"
_ambient = "0xffffff"
_emisive = "0x000000"
_specular = "0x444444"
_shininess = 100
_transparent = "false"
_opacity = 1.0
_smooth = False

_p_mat_str = """\
var material = new THREE.PointCloudMaterial({{
  color : {},
  size : {},
  sizeAttenuation : false,
  fog : true
}});
"""

_p_geo_str = """\
var geometry = new THREE.Geometry();
geometry.vertices.push(
  {}
);
"""

_p_add_str = """\
var points = new THREE.PointCloud( geometry, material);
scene.add( points);
"""

_l_mat_str = """\
var material = new THREE.LineBasicMaterial({{
  color : {},
  linewidth : {},
  fog : true
}});
"""

_l_geo_str = _p_geo_str

_l_add_str = """\
var line = new THREE.Line( geometry, material);
scene.add( line);
"""

_m_mat_str = """\
var material = new THREE.MeshPhongMaterial( {{
  color : {},
  ambient : {},
  specular : {},
  emissive : {},
  shininess : {},
  transparent : {},
  opacity : {},
  side: THREE.DoubleSide,
  wireframe : false,
  fog : true,
}});
"""

_m_geo_str = """\
var geometry = new THREE.Geometry();
geometry.vertices.push(
  {}
);
geometry.faces.push(
  {}
);
geometry.computeFaceNormals();
"""

_m_smooth_str = """\
geometry.computeVertexNormals();
"""

_m_add_str = """\
var mesh = new THREE.Mesh( geometry, material);
scene.add( mesh);
"""

_html_wrapper = """\
<html>
  <head>
    <title>Test Three.js app</title>
  </head>
  <body>
    {PLOT_HTML}
  </body>
</html>
"""

_canvas = """
<canvas 
  id="{UUID}" 
  width="600" 
  height="400"
>
</canvas>
<script type="text/javascript" src="js/three.min.js"></script>
<script type="text/javascript" src="js/TrackBallControls.js"></script>
<script type="text/javascript" src="js/OrbitControls.js"></script>
{SCRIPT_MAIN}
"""

_script_main = """
<script>
  var canvas = 
    document.getElementById("{UUID}");

  var camera, controls; 
  var scene, renderer;

  renderer = new THREE.WebGLRenderer({{ 
    canvas: canvas,
    alpha: true,
    antialiasing: true
  }});
  renderer.setSize( canvas.width, canvas.height);

  scene = new THREE.Scene();

  init_camera();
  init_lights();
  init_controls();
  init_scene();

  render();
  animate();

  {INIT_CAMERA}
  {INIT_LIGHTS}
  {INIT_CONTROLS}
  {INIT_SCENE}
  {RENDER}
  {ANIMATE}
</script>
"""

_init_camera = """
function init_camera() {{
  camera = new THREE.PerspectiveCamera( 
    45, 
    canvas.width/canvas.height, 
    0.1, 
    100
  );
  camera.position.set( {POS} ); 
  camera.up = {UP};
  camera.lookAt( {LOOKAT} );
}}
"""

_camera_up = Vector3([0, 0, 1])

_init_lights = """
function init_lights() {
  var light = new THREE.DirectionalLight( 0x882222 );
  camera.add( light );
  light.position.set( 0, 100., 30. );

  light = new THREE.DirectionalLight( 0x228822 );
  camera.add( light );
  light.position.set( 60., 80., 30. );

  light = new THREE.DirectionalLight( 0x222288 );
  camera.add( light );
  light.position.set( 0., 80., 90. );

  light = new THREE.AmbientLight( 0x444444 );
  scene.add( light );
  scene.add( camera );
}
"""

_init_controls = """
function init_controls() {{
  controls = new THREE.OrbitControls( camera, canvas );
  controls.rotateSpeed = 5.0;
  controls.zoomSpeed = 1.2;
  controls.noZoom = false;
  controls.noPan = true;
  controls.staticMoving = true;
  controls.dynamicDampingFactor = 0.3;
  controls.addEventListener( 'change', render ); 
  controls.target.set( {LOOKAT} );
}}
"""

_init_scene = """
function init_scene() {{
 {GEOMETRY_OBJECTS}
}}
"""

_render = """
function render(){
  renderer.render(scene, camera);
}
"""

_animate = """
function animate(){
  requestAnimationFrame( animate );
  controls.update();        
}
"""

if __name__ == '__main__':
  import os
  import webbrowser
  m = Mesh([[[0,0,0],[1,0,0],[1,1,0],[0,1,0],
             [0,0,1],[1,0,1],[1,1,1],[0,1,1]],
             [0,1,2,3,4,5,6,7],
            [[0,1],[1,2],[2,3],[3,0],
             [0,4],[1,5],[2,6],[3,7],
             [4,5],[5,6],[6,7],[7,4]],
            [[0,1,2],[0,2,3],[0,4,1],[1,4,5],
             [1,5,2],[2,5,6],[2,6,3],[3,6,7],
             [3,7,0],[0,7,4],[4,6,5],[6,4,7]]])
  center = Vector3( 1/2, 1/2, 1/2)
  pos = Vector3( -3, 10, 3)
  uu = uuid()
  cam = _init_camera.format( POS=pos, UP=_camera_up.THREEjs(),
                            LOOKAT=center.THREEjs() )
  controls = _init_controls.format( LOOKAT=center )
  scene = _init_scene.format( GEOMETRY_OBJECTS = m.toTHREEjs() )
  script = _script_main.format(
      UUID = uu,
      INIT_CAMERA = cam,
      INIT_LIGHTS = _init_lights,
      INIT_CONTROLS = controls,
      INIT_SCENE = scene,
      RENDER = _render,
      ANIMATE = _animate
    )
  canvas = _canvas.format( UUID = uu, SCRIPT_MAIN = script )
  webpage = _html_wrapper.format( PLOT_HTML = canvas )
  f = open('temp.html', 'w+b')
  f.write(webpage.encode('utf-8'))
  f.close()
  webbrowser.open('file://'+os.path.realpath(f.name))

