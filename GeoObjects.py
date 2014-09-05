import math
import copy


# Copy all data from objSource to objDest.
#
# This function is useful for copy constructors.
def copyFromObject( objDest, objSource):
  """General copy object function"""
  for attr in objSource.__dict__:
    setattr( objDest, attr, copy.deepcopy(getattr(args[0].attr)))

# Simple arithmatic function for numbers in list
def listNeg( l):
  return [-x for x in l]

def listAdd( l1, l2):
  return [x+y for x,y in zip(l1,l2)]

def listSub( l1, l2):
  return [x-y for x,y in zip(l1,l2)]

def scalarMul( a, l):
  return [a*x for x in l]

# A class for 3 component vectors
#
# A class to make manipulating three vectors easier. It contains
# methods for inner product, cross product, magnitude, finding the
# normal vector, as well as overloading the negative, addition,
# subtraction with the appropriate list arithmatic function, and
# overloading the multiplicaiton with either the inner product or
# scalar multiplicaiton depending they type of the argument.
class Vector3:
  """A 3 component vector of real numbers"""

  def __init__(self, *args):
    """Constructor from either Vector3, iterable, or x y and z"""
    if len(args) == 1:
      self.v = [float(x) for x in args[0][:3]]
    elif len(args) == 3:
      self.v = [float(x) for x in args[:3]]
    else:
      raise ValueError("Vector3.__init__ take 1 or 3 arguments")

  def __iter__(self):
    """Iterate x to y to z"""
    return iter(self.v[:])

  def __str__(self):
    """Print the components"""
    return "{}, {}, {}".format(self.v[0],self.v[1],self.v[2])

  def inner(self, other):
    """Inner product of two vectors"""
    return sum([x*y for x,y in zip(self.v, other.v)])

  def cross(self, other):
    """Cross product of two vectors"""
    x = self.v[1]*other.v[2]-self.v[2]*other.v[1]
    y = self.v[2]*other.v[0]-self.v[0]*other.v[2]
    z = self.v[0]*other.v[1]-self.v[1]*other.v[0]
    return Vector3(x,y,z)

  def __add__(self, other):
    if isinstance(other, Vector3):
      return Vector3( [x+y for x,y in zip( self.v, other.v)])
    else:
      return Vector3( [x+other for x in self.v])

  __radd__ = __add__

  def __sub__(self, other):
    if isinstance(other, Vector3):
      return Vector3( [x-y for x,y in zip( self.v, other.v)])
    else:
      return Vector3( [x-other for x in self.v])

  def __rsub__(self, other):
    if isinstacne(other, Vector3):
      return Vector3( [y-x for x,y in zip( self.v, other.v)])
    else:
      return Vector3( [other-x for x in self.v])

  def __neg__(self):
    return Vector3( [-x for x in self.v])

  def __mul__(self, other):
    if isinstance(other, Vector3):
      return self.inner(other)
    else:
      return Vector3( scalarMul( float(other), self.v))

  __rmul__ = __mul__

  def __truediv__(self, other):
    return Vector3( scalarMul( 1./float(other), self.v))

  def mag(self):
    """Magnitude of a vector"""
    return math.sqrt( sum( [x*x for x in self.v]))

  def norm(self):
    """Normalized vector"""
    return self/mag(self)

# A simple casting function
def vec3( *args):
  if len(args) == 1 and isinstance(args[0], Vector3):
    return args[0]
  else:
    return Vector3(*args)

# A few convenience functions
#
# The dot, cross, mag, and norm functions as wrappers to the Vector3
# class methods of the same names.
def dot( v1, v2):
  return v1.inner(v2)

def cross( v1, v2):
  return v1.cross(v2)

def mag( v):
  return v.mag()

def norm( v):
  return v.norm()

# A class for 4x4 matrices.
#
# Overload the negation, addition, subtractions, and left and right
# multiplication operations.
class Matrix4:
  """A 4x4 matrix of real numbers"""

  def __init__(self, *args):
    if len(args) == 1:
      self.m = [[float(y) for y in x] for x in args[0][:4]]
    elif len(args) == 4:
      self.m = [[float(y) for y in x] for x in args[:4]]
    elif len(args) == 16:
      self.m = []
      for i in range(4):
        self.m[i] = [float(x) for x in args[i:i+4]]
    else:
      raise ValueError("Matrix4.__init__ take 1 or 4 arguments")

  def __neg__(self):
    return Matrix4( [[-a for a in row] for row in self.m])

  def __add__(self, other):
    return Matrix4( [[a+b for a,b in zip(rowA,rowB)] 
                      for rowA,rowB in zip(self.m,other.m)])
  __radd__ = __add__

  def __sub__(self, other):
    return Matrix4( [[a-b for a,b in zip(rowA,rowB)]
                      for rowA,rowB in zip(self.m,other.m)])

  __rsub__ = __sub__

  def matMul(self, other):
    return Matrix4( [[sum([a*b for a,b, in zip(row,column)])
                      for row in other.m] for column in zip(*(self.m))])

  def scalarMul(self, other):
    return Matrix4( [[float(other)*a for a in row] for row in self.m])

  def __mul__(self, other):
    if isinstance(other, Matrix4):
      return self.matMul(other)
    else:
      return self.scalarMul(other)

  def __rmul__(self, other):
    if isinstance(other, Matrix4):
      return other.matMul(self)
    else:
      return self.scalarMul(other)

# 4x4 matricies transformations
#
# This is the end.
def scale( *args):
  """Scale all coordinates by s, or x y and z by sx sy and sz
  respectively"""
  if len(args) == 1:
    s = float(args[0])
    return Matrix4([s,0,0,0],[0,s,0,0],[0,0,s,0],[0,0,0,1])
  elif len(args) == 3:
    sx,sy,sz = [float(x) for x in args[:3]]
    return Matrix4([sx,0,0,0],[0,sy,0,0],[0,0,sz,0],[0,0,0,1])

def translate( *args):
  """Translate all coordinates by vector (dx, dy, dz)"""
  if len(args) == 1 and isinstance( args[0], Vector3):
    dx,dy,dz = args[0].v
  elif len(args) == 1:
    dx,dy,dz = [float(x) for x in args[0][:3]]
  else:
    dx,dy,dz = [float(x) for x in args[:3]]
  return Matrix4([1,0,0,dx],[0,1,0,dy],[0,0,1,dz],[0,0,0,1])

def rotateZ( angle):
  """Rotation around the z axis"""
  s = math.sin(angle)
  c = math.cos(angle)
  return Matrix4([c,-s,0,0],[s,c,0,0],[0,0,1,0],[0,0,0,1])

def rotateY( angle):
  """Rotation around the y axis"""
  s = math.sin(angle)
  c = math.cos(angle)
  return Matrix4([c,0,s,0],[0,1,0,0],[-s,0,c,0],[0,0,0,1])

def rotateX( angle):
  """Rotation around the x axis"""
  s = math.sin(angle)
  c = math.cos(angle)
  return Matrix4([1,0,0,0],[0,c,-s,0],[0,s,c,0],[0,0,0,1])

def rotateAA( axis, angle):
  """Rotation around a vector"""
  vtemp = vec3( axis)
  u = norm( vtemp)
  ux,uy,uz = u.v
  c = math.sin(angle)
  s = math.cos(angle)
  rx = [c + ux*ux*(1-c), ux*uy*(1-c) - uz*s, ux*uz*(1-c) + uy*s, 0]
  ry = [uy*ux*(1-c) + uz*s, c + uy*uy*(1-c), uy*uz*(1-c) - ux*s, 0]
  rz = [uz*ux*(1-c) - uy*s, uz*uy*(1-c) + ux*s, c + uz*uz*(1-c), 0]
  rw = [0,0,0,1]
  return Matrix4( rx, ry, rz, rw)

def new3jsVector3( v):
  return "new THREE.Vector3({})".format(vec3(v))

def new3jsFace3( *args):
  if len(args) == 1:
    i0,i1,i2 = args[0][:3]
  else:
    i0,i1,i2 = args[:3]
  return "new THREE.Face3({},{},{})".format(i0,i1,i2)

class GeoVertObj:
  """A base class for GeoObj base on vertices"""

  def boundingBox(self):
    """The bounding box given as two Vector3's that hold the minimum
    and maximum x, y, and z coordinates."""
    x = [vert.v[0] for vert in self.vertices]
    y = [vert.v[1] for vert in self.vertices]
    z = [vert.v[2] for vert in self.vertices]
    vmin = Vector3( min(x), min(y), min(z))
    vmax = Vector3( max(x), max(y), min(z))
    return (vmin, vmax)

def totalBoundingBox( bb):
  """Give the total bounding box for a list of bounding boxes"""
  vtmin, vtmax = bb[0];
  for vmin, vmax in bb[1:]:
    for i in range(3):
      vtmin.v[i] = min( vtmin.v[i], vmin.v[i])
      vtmax.v[i] = max( vtmax.v[i], vmax.v[i])
  return (vtmin, vtmax)

_tsDefaultDict = {
  "color" : "0xcccccc",
  "ambient" : "0xffffff",
  "emissive" : "0x000000",
  "specular" : "0x444444",
  "shininess" : 100,
  "opacity" : 1.0,
  "smooth" : True
}

class TriangleSet(GeoVertObj):
  """A list of vertices, and a list of faces contructed from the
  vertices"""

  def __init__(self, *args, **kwargs):
    if len(args) == 1:
      self.vertices = [vec3(x) for x in args[0][1]]
      self.faces = [[int(x) for x in face[:3]] for face in args[0][2]]
    elif len(args) == 2:
      self.vertices = [vec3(x) for x in args[0]]
      self.faces = [[int(x) for x in face[:3]] for face in args[1]]
    for attr in _tsDefaultDict:
      if attr in kwargs:
        setattr( self, attr, kwargs[attr])
      else:
        setattr( self, attr, _tsDefaultDict[attr])

  def faceCenter(self, face):
    """The geometric center of face"""
    v0, v1, v2 = [self.vertices[i] for i in face]
    return (v0+v1+v2)/3

  def faceArea(self, face):
    """The area of the face"""
    v0, v1, v2 = [self.vertices[i] for i in face]
    e1 = v1-v0
    e2 = v2-v0
    return 0.5*mag(cross(e1,e2))

  def stats(self):
    """Returns and ordered pair that give the sum of the area weighted
    centers of the faces, and the total area."""
    fc = [self.faceCenter(face) for face in self.faces]
    fa = [self.faceArea(face) for face in self.faces]
    num = sum([x*y for x, y in zip(fc, fa)])
    denom = sum(fa)
    return (num, denom)

  tsScene = """\
  var material = new THREE.MeshPhongMaterial( {{
    color : {COLOR},
    ambient : {AMBIENT},
    specular : {SPECULAR},
    emissive : {EMISSIVE},
    shininess : {SHININESS},
    transparent : {TRANSPARENT},
    opacity : {OPACITY},
    side: THREE.DoubleSide,
    wireframe : false,
    fog : true,
  }});
  var geometry = new THREE.Geometry();
  geometry.vertices.push(
    {VERTEX_LIST}
  );
  geometry.faces.push(
    {FACE_LIST}
  );
  geometry.computeFaceNormals();
  {SMOOTH}
  var mesh = new THREE.Mesh( geometry, material);
  scene.add( mesh);
  """

  def render(self):
    vertStr = [new3jsVector3(v) for v in self.vertices]
    vertStr = ",\n  ".join(vertStr)
    faceStr = [new3jsFace3(f) for f in self.faces]
    faceStr = ",\n  ".join(faceStr)
    if self.opacity < 1.:
      self.transparent = True
    else:
      self.transparent = False
    if self.smooth:
      smoothStr = "geometry.computeVertexNormals();"
    else:
      smoothStr = ""
    return (self.tsScene.format(
              COLOR = self.color,
              AMBIENT = self.ambient,
              SPECULAR = self.specular,
              EMISSIVE = self.emissive,
              SHININESS = "{}".format(self.shininess),
              TRANSPARENT = ("false","true")[self.transparent],
              OPACITY = "{}".format(self.opacity),
              VERTEX_LIST = vertStr,
              FACE_LIST = faceStr,
              SMOOTH = smoothStr
            ))

_lDefaultDict = {
  "lineColor" : '0x000000',
  "lineWidth" : 2.,
  "closed" : False
}

class Line(GeoVertObj):
  """An ordered list of vertices with a line drawn between them."""

  def __init__(self, *args, **kwargs):
    if len(args) == 1:
      self.vertices = [vec3(x) for x in args[0][:]]
    else:
      self.vertices = [vec3(x) for x in args[:]]
    for attr in _lDefaultDict:
      if attr in kwargs:
        setattr( self, attr, kwargs[attr])
      else:
        setattr( self, attr, _lDefaultDict[attr])
    if self.closed:
      self.vertices = self.vertices + [self.vertices[0]]


  def lineCenter(self, lineIndex):
    v0, v1 = self.vertices[lineIndex:lineIndex+2]
    return 0.5*(v0+v1)

  def lineLength(self, lineIndex):
    v0, v1 = self.vertices[lineIndex:lineIndex+2]
    return mag(v0-v1)

  def stats(self):
    lc = [self.lineCenter(i) for i in range(0,len(self.vertices)-1)]
    ll = [self.lineLength(i) for i in range(0,len(self.vertices)-1)]
    num = sum([x*y for x,y in zip(lc,ll)])
    denom = sum(ll)
    return (num, denom)

  lScene = """\
  var material = new THREE.LineBasicMaterial({{
    color : {LINE_COLOR},
    linewidth : {LINE_WIDTH},
    fog : true
  }});
  var geometry = new THREE.Geometry();
  geometry.vertices.push(
    {VERTEX_LIST}
  );
  var line = new THREE.Line( geometry, material);
  scene.add( line);
  """

  def render(self):
    vertStr = [new3jsVector3(v) for v in self.vertices]
    vertStr = ",\n  ".join(vertStr)
    return (self.lScene.format(
              LINE_COLOR = self.lineColor,
              LINE_WIDTH = "{}".format(self.lineWidth),
              VERTEX_LIST = vertStr
            ))

_pDefaultDict = {
  "pointColor" : 'rgb(0,0,0)',
  "pointEdgeWidth" : 1.,
  "pointEdgeColor" : False,
  "pointSize" : 1.,
  "pointStyle" : 'circle'
}

class Point(GeoVertObj):
  def __init__(self, *args, **kwargs):
    self.vertices = [vec3(x) for x in args[:]]
    for attr in _pDefaultDict:
      if attr in kwargs:
        setattr( self, attr, kwargs[attr])
      else:
        setattr( self, attr, _pDefaultDict[attr])
    if self.pointStyle == 'x' or self.pointStyle == '+':
      self.pointColor = False
      if not self.pointEdgeColor:
        self.pointEdgeColor = 'rgb(0,0,0)'

  def stats(self):
    num = sum(self.vertices)
    return (num, len(self.vertices))

  pCanv = """\
    var canv = document.createElement('canvas');
    var pointSize = 5*{POINT_SIZE};
    var canvSize = pointSize+2*{EDGE_WIDTH}+2;
    canv.width = canvSize;
    canv.height = canvSize;
    var cc = canvSize/2;
    var ro = pointSize/2;
    var context = canv.getContext('2d');
    context.beginPath();
    """
  pointStyles = {
    "circle" : """\
    var rc = 0.5*Math.sqrt(2)*ro;
    context.arc(cc,cc,rc,0,2*Math.PI,true);
    """,
    "disk" : """\
    var rc = 0.5*Math.sqrt(2)*ro;
    context.arc(cc,cc,rc,0,2*Math.PI,true);
    """,
    "square" : """\
    context.moveTo((cc-ro*0.5*Math.sqrt(2)),(cc-ro*0.5*Math.sqrt(2)));
    context.lineTo((cc+ro*0.5*Math.sqrt(2)),(cc-ro*0.5*Math.sqrt(2)));
    context.lineTo((cc+ro*0.5*Math.sqrt(2)),(cc+ro*0.5*Math.sqrt(2)));
    context.lineTo((cc-ro*0.5*Math.sqrt(2)),(cc+ro*0.5*Math.sqrt(2)));
    context.closePath();
    """,
    "diamond" : """\
    context.moveTo(cc,cc-ro);
    context.lineTo(cc+ro,cc);
    context.lineTo(cc,cc+ro);
    context.lineTo(cc-ro,cc);
    context.closePath();
    """,
    "triangle" : """\
    context.moveTo((cc-ro*0.5*Math.sqrt(3)),(cc-ro*0.5));
    context.lineTo((cc+ro*0.5*Math.sqrt(3)),(cc-ro*0.5));
    context.lineTo(cc,cc+ro);
    context.closePath();
    """,
    "upTriangle" : """\
    context.moveTo((cc-ro*0.5*Math.sqrt(3)),(cc-ro*0.5));
    context.lineTo((cc+ro*0.5*Math.sqrt(3)),(cc-ro*0.5));
    context.lineTo(cc,cc+ro);
    context.closePath();
    """,
    "downTriangle" : """\
    context.moveTo(cc,cc-ro);
    context.lineTo((cc+ro*0.5*Math.sqrt(3)),(cc+ro*0.5));
    context.lineTo((cc-ro*0.5*Math.sqrt(3)),(cc+ro*0.5));
    context.closePath();
    """,
    "star" : """\
    var th = Math.PI/5;
    var phi = (1 + Math.sqrt(5))/2;
    var ri = ro/(phi*phi);
    context.moveTo(cc,cc+ro);
    context.lineTo(cc+ri*Math.sin(1*th),cc+ri*Math.cos(1*th));
    context.lineTo(cc+ro*Math.sin(2*th),cc+ro*Math.cos(2*th));
    context.lineTo(cc+ri*Math.sin(3*th),cc+ri*Math.cos(3*th));
    context.lineTo(cc+ro*Math.sin(4*th),cc+ro*Math.cos(4*th));
    context.lineTo(cc+ri*Math.sin(5*th),cc+ri*Math.cos(5*th));
    context.lineTo(cc+ro*Math.sin(6*th),cc+ro*Math.cos(6*th));
    context.lineTo(cc+ri*Math.sin(7*th),cc+ri*Math.cos(7*th));
    context.lineTo(cc+ro*Math.sin(8*th),cc+ro*Math.cos(8*th));
    context.lineTo(cc+ri*Math.sin(9*th),cc+ri*Math.cos(9*th));
    context.closePath();
    """,
    "x" : """\
    context.moveTo((cc-ro*0.5*Math.sqrt(2)),(cc-ro*0.5*Math.sqrt(2)));
    context.lineTo((cc+ro*0.5*Math.sqrt(2)),(cc+ro*0.5*Math.sqrt(2)));
    context.moveTo((cc+ro*0.5*Math.sqrt(2)),(cc-ro*0.5*Math.sqrt(2)));
    context.lineTo((cc-ro*0.5*Math.sqrt(2)),(cc+ro*0.5*Math.sqrt(2)));
    """,
    "+" : """\
    context.moveTo(cc,cc-ro);
    context.lineTo(cc,cc+ro);
    context.moveTo(cc+ro,cc);
    context.lineTo(cc-ro,cc);
    """
  }
  pointFill = """\
  context.fillStyle = '{POINT_COLOR}';
  context.fill();
  """
  pointStroke = """\
  context.lineWidth = {EDGE_WIDTH};
  context.strokeStyle = '{EDGE_COLOR}';
  context.stroke();
  """

  pScene = """\
  var texture = new THREE.Texture(canv);
  texture.needsUpdate = true;
  var material = new THREE.PointCloudMaterial({{
    map: texture,
    transparent: true,
    size: canvSize,
    sizeAttenuation: false,
    fog: true
  }});
  material.alphaTest = 0.05;
  var geometry = new THREE.Geometry();
  geometry.vertices.push(
    {VERTEX_LIST}
  )
  var point = new THREE.PointCloud(geometry, material);
  point.sortParticles = true;
  scene.add( point);
  """

  def render(self):
    canvStr = self.pCanv.format(POINT_SIZE = self.pointSize,
                                EDGE_WIDTH = self.pointEdgeWidth)
    canvStr = canvStr + self.pointStyles[self.pointStyle]
    if self.pointColor:
      canvStr = canvStr + self.pointFill.format(
          POINT_COLOR = self.pointColor)
    if self.pointEdgeColor:
      canvStr = canvStr + self.pointStroke.format(
          EDGE_WIDTH = self.pointEdgeWidth,
          EDGE_COLOR = self.pointEdgeColor)
    vertStr = [new3jsVector3(v) for v in self.vertices]
    vertStr = ",\n  ".join(vertStr)
    sceneStr = self.pScene.format(
        VERTEX_LIST = vertStr)
    return (canvStr + sceneStr)
  # pMaterial = """\
  # var texture = new THREE.Texture(canv);
  # texture.needsUpdate = true;
  # var material = new THREE.SpriteMaterial({
  #   map: texture,
  #   fog: true
  # });
  # """
  # pSprite = """\
  # var sprite = new THREE.Sprite( material);
  # sprite.position.set( {POSITION});
  # sprite.scale.set( {POINT_SIZE}*.075, {POINT_SIZE}*.075, 1);
  # scene.add( sprite);
  # """

_tDefaultDict = {
  "font" : 'Helvetica',
  "fontSize" : '10',
  "textColor" : 'rgb(0,0,0)',
  "textMargin" : 5.,
  "textBackgroundColor" : False,
  "textEdgeWidth" : 1.,
  "textEdgeColor" : False,
  "textPoint" : 'center'
}

class Text(GeoVertObj):
  def __init__(self,text,*pos,**kwargs):
    self.text = text;
    self.vertices = [vec3(*pos)];
    for attr in _tDefaultDict:
      if attr in kwargs:
        setattr( self, attr, kwargs[attr])
      else:
        setattr( self, attr, _tDefaultDict[attr])

  def stats(self):
    return ( self.vertices[0], 1)

  tCanv = """\
  var canv = document.createElement('canvas');
  var context = canv.getContext('2d');
  var boarderWidth = {EDGE_WIDTH};
  var margin = {MARGIN};
  var textHeight = {TEXT_SIZE};
  var text = "{TEXT}";
  var font = '{FONT}';
  context.font = textHeight + 'pt ' + font;
  var metrics = context.measureText( text);
  var textWidth = metrics.width;
  var rectHeight = 2*margin + textHeight;
  var rectWidth = 2*margin + textWidth;
  var canvSize = 2*(boarderWidth+1+Math.max(rectHeight,rectWidth));
  canv.height = canvSize;
  canv.width = canvSize;
  context.translate( canvSize/2 , canvSize/2);
  context.scale(1,-1);
  context.lineWidth = 10;
  context.strokeRect( -canvSize/2, -canvSize/2, canvSize, canvSize);
  """
  tCanvSize = {
    "center" : """\

    """,
    "top" : """\
    context.translate( 0, rectHeight/2);
    """,
    "bottom" : """\
    context.translate( 0, -rectHeight/2);
    """,
    "left" : """\
    context.translate( rectWidth/2, 0);
    """,
    "right" : """\
    context.translate( -rectWidth/2, 0);
    """,
    "topLeft" : """\
    context.translate( rectWidth/2, rectHeight/2);
    """,
    "topRight" : """\
    context.translate( -rectWidth/2, rectHeight/2);
    """,
    "bottomLeft" : """\
    context.translate( rectWidth/2, -rectHeight/2);
    """,
    "bottomRight" : """\
    context.translate( -rectWidth/2, -rectHeight/2);
    """
  }
  tRectFill = """\
  context.rect(-rectWidth/2, -rectHeight/2, rectWidth, rectHeight);
  context.fillStyle = '{BACKGROUND_COLOR}';
  context.fill();
  """
  tRectStroke = """\
  context.rect(-rectWidth/2, -rectHeight/2, rectWidth, rectHeight);
  context.strokeStyle = '{EDGE_COLOR}';
  context.lineWidth = boarderWidth;
  context.stroke();
  """
  tScene = """\
  context.font = textHeight + 'pt ' + font;
  context.fillStyle = '{TEXT_COLOR}';
  context.textAlign = 'center';
  context.textBaseline = 'middle';
  context.fillText( text, 0, 0);
  var texture = new THREE.Texture(canv);
  texture.needsUpdate = true;
  var material = new THREE.PointCloudMaterial({{
    map: texture,
    transparent: true,
    size: 40,
    sizeAttenuation: false,
    fog: true
  }});
  console.log( canvSize);
  console.log( material.size);
  material.alphaTest = 0.1;
  var geometry = new THREE.Geometry();
  geometry.vertices.push(
    new THREE.Vector3({POSITION})
  )
  var point = new THREE.PointCloud(geometry, material);
  point.sortParticles = true;
  scene.add( point);
  """

  def render(self):
    canvStr = self.tCanv.format(EDGE_WIDTH = self.textEdgeWidth,
                                MARGIN = self.textMargin,
                                TEXT_SIZE = self.fontSize,
                                TEXT = self.text,
                                FONT = self.font)
    canvStr = canvStr + self.tCanvSize[self.textPoint]
    if self.textBackgroundColor:
      canvStr = canvStr + self.tRectFill.format(
          BACKGROUND_COLOR = self.textBackgroundColor)
    if self.textEdgeColor:
      canvStr = canvStr + self.tRectStroke.format(
          EDGE_COLOR = self.textEdgeColor)
    sceneStr = self.tScene.format(
        TEXT_COLOR = self.textColor,
        POSITION = self.vertices[0])
    return (canvStr + sceneStr)


defaultLighting = """\
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
"""

htmlWrapper = """\
<html>
  <head>
    <title>Test Three.js app</title>
  </head>
  <body>
{SCRIPT}
  </body>
</html>
"""

#<script type="text/javascript" src="js/three.min.js"></script>
#<script type="text/javascript" src="js/TrackBallControls.js"></script>
#<script type="text/javascript" src="js/OrbitControls.js"></script>
fullScript = """\
<script type="text/javascript" src="js/three.min.js"></script>
<script type="text/javascript" src="js/TrackBallControls.js"></script>
<script type="text/javascript" src="js/OrbitControls.js"></script>
<canvas 
  id="{UUID}" 
  width="600" 
  height="400"
>
</canvas>

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

function init_camera() {{
  camera = new THREE.PerspectiveCamera( 
    {FOV}, 
    canvas.width/canvas.height, 
    {FRONTPLANE}, 
    {BACKPLANE}
  );
  camera.position.set( {POS} ); 
  camera.up = new THREE.Vector3({UP});
  camera.lookAt( new THREE.Vector3({TARGET}) );
}}

function init_lights() {{
{LIGHTS}
}}  

function init_controls() {{
  controls = new THREE.OrbitControls( camera, canvas );
  controls.rotateSpeed = 5.0;
  controls.zoomSpeed = 1.2;
  controls.noZoom = false;
  controls.noPan = true;
  controls.staticMoving = true;
  controls.dynamicDampingFactor = 0.3;
  controls.addEventListener( 'change', render ); 
  controls.target.set( {TARGET} );
}}

function init_scene() {{
{SCENE}
}}

function render(){{
  renderer.render(scene, camera);
}}

function animate(){{
  requestAnimationFrame( animate );
  controls.update();        
}}
</script>
"""

from uuid import uuid4 as uuid

_rDefaultDict = {
  "cameraFOV" : math.pi/8.,
  "cameraFrontPlane" : 0.1,
  "cameraBackPlane" : 1000.,
  "cameraUp" : Vector3( 0, 0, 1),
  "cameraTheta" : 2.*math.pi/5.,
  "cameraPhi" : -math.pi/10.,
  "lighting" : defaultLighting
}

def render( *geoObjs, **kwargs):
  renderD = {}
  for key in _rDefaultDict:
    if key in kwargs:
      renderD[key] = kwargs[key]
    else:
      renderD[key] = _rDefaultDict[key]
  # Find the bounding box
  bb = [x.boundingBox() for x in geoObjs]
  vmin, vmax = totalBoundingBox(bb)
  # Find the maximum distance between points
  maxWidth = mag(vmax-vmin)
  # Find the center of rendering
  if "cameraTarget" in kwargs:
    renderD["cameraTarget"] = vec3( kwargs["cameraTarget"])
  else:
    dw = maxWidth/20.
    num = 0.;
    denom = 0.;
    for geoObj in geoObjs:
      objNum, objDenom = geoObj.stats();
      if isinstance( geoObj, Line):
        objNum *= dw
        objDenom *= dw
      if isinstance( geoObj, Point) or isinstance( geoObj, Text):
        objNum *= dw*dw
        objDenom *= dw*dw
      num += objNum
      denom += objDenom
    renderD["cameraTarget"] = num/denom;
  # Find the position of the camera
  if "cameraPosition" in kwargs:
    renderD["cameraPosition"] = vec3( kwargs["cameraPosition"])
  else:
    cameraDist = maxWidth/(math.sin(renderD["cameraFOV"])/2)
    if "cameraVector" in kwargs:
      renderD[cameraVector] = norm(vec3(kwargs["cameraVector"]))
    else:
      th = renderD["cameraTheta"]
      phi = renderD["cameraPhi"]
      renderD["cameraVector"] = Vector3( math.sin(th)*math.cos(phi),
                                           math.sin(th)*math.sin(phi),
                                           math.cos(th))
    renderD["cameraPosition"] = (renderD["cameraTarget"] + 
                                 cameraDist*renderD["cameraVector"])
  # Get the geometry string
  geometry = ""
  for geoObj in geoObjs:
    geometry = geometry+geoObj.render()
  #
  uu = uuid()
  return (fullScript.format(
            UUID = uu,
            FOV = 180./math.pi*renderD["cameraFOV"],
            FRONTPLANE = renderD["cameraFrontPlane"],
            BACKPLANE = renderD["cameraBackPlane"],
            POS = renderD["cameraPosition"],
            UP = renderD["cameraUp"],
            TARGET = renderD["cameraTarget"],
            LIGHTS = renderD["lighting"],
            SCENE = geometry
          ))

