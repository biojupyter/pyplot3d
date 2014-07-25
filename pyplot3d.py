import os
import tempfile
import webbrowser
import time
from uuid import uuid4 as uuid

class Vector3:
  def __init__(self):
    self.x = 0.
    self.y = 0.
    self.z = 0.

  def __init__(self, x, y, z):
    self.x = x
    self.y = y
    self.z = z

  def __init__(self, v):
    self.x = v.x
    self.y = v.y
    self.z = v.z

  def length(self):
    math.sqrt( self.x*self.x + self.y*self.y + self.z*self.z )

  def scalar_mul(self, a):
    self.x *= a
    self.y *= a
    self.z *= a

  def normalize(self):
    l = self.length()
    if( l != 0 ):
      self.scalar_mul( 1./l )

  def dot(self, v):
    self.x*v.x + self.y*v.y + self.z*v.z

  def cross(self, v):
    self.x = self.y*v.z - self.z*v.y
    self.y = self.z*v.x - self.x*v.z
    self.z = self.x*v.y - self.y*v.x

  def tup(self):
    self.x, self.y, self.z

def dot(v1, v2):
  v1.x*v2.x + v1.y*v2.y + v1.z*v2.z

def cross(v1, v2):
  v = Vector3( v1)
  v.cross( v2)

class Point:
  def __init__(self, *args):
    self.p = Vector3( *args)

  def transform(self, t):
    self.p.transform( t)

html_wrapper = """<html>
  <head>
    <title>Test Three.js app</title>
  </head>
  <body>
    {PLOT_HTML}
  </body>
</html>
"""

plot_html = """
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

script_main = """
    <script>

      var canvas = 
        document.getElementById("{UUID}");

      var camera, controls; 
      var scene, renderer;

      renderer = new THREE.WebGLRenderer({{ 
        canvas: canvas,
        alpha: true
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

script_init_camera = """
      function init_camera() {
        camera = new THREE.PerspectiveCamera( 
          75, 
          canvas.width/canvas.height, 
          0.1, 
          100
        );
        camera.position.set( -3., 10., 3. ); 
        camera.up = new THREE.Vector3( 0, 0, 1 );
        camera.lookAt( new THREE.Vector3( 0, 0, 0 ) );
      }
"""

script_init_lights = """
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

script_init_controls = """
      function init_controls() {
        controls = new THREE.OrbitControls( camera, canvas );

        controls.rotateSpeed = 5.0;
        controls.zoomSpeed = 1.2;

        controls.noZoom = false;
        controls.noPan = true;

        controls.staticMoving = true;
        controls.dynamicDampingFactor = 0.3;

        controls.addEventListener( 'change', render );        
      }
"""

script_init_scene = """
      function init_scene() {

        var material = new THREE.MeshPhongMaterial( {
          specular: 0x444444,
          color: 0xcccccc,
          emissive: 0x000000,
          shininess: 100
        });

        var geometry = new THREE.SphereGeometry( 1, 32, 32 );

        var sphere = new THREE.Mesh( geometry, material );
        scene.add( sphere );
        geometry = new THREE.BoxGeometry( 0.8, 0.9, 1. );
        var cube = new THREE.Mesh( geometry, material );
        cube.position.set( -1, -1, -1 );
        scene.add( cube );
      }
"""

script_render = """
      function render(){
        renderer.render(scene, camera);
      }
"""

script_animate = """
      function animate(){
        requestAnimationFrame( animate );
        controls.update();        
      }
"""

if __name__ == '__main__':
  # f = tempfile.NamedTemporaryFile(suffix='.html')
  f = open('temp.html', 'w+b')
  uu = uuid()
  text = script_main.format(UUID=uu,
                            INIT_CAMERA=script_init_camera,
                            INIT_LIGHTS=script_init_lights,
                            INIT_CONTROLS=script_init_controls,
                            INIT_SCENE=script_init_scene,
                            RENDER=script_render,
                            ANIMATE=script_animate)
  text = plot_html.format(UUID=uu, SCRIPT_MAIN=text)
  text = html_wrapper.format(PLOT_HTML=text)
  print( f.name)
  f.write(text.encode('utf-8'))
  f.close()
  webbrowser.open('file://'+os.path.realpath(f.name))


