import numpy as np
import open3d as o3d
import copy

# load obj
def load_obj(path, texture_path=None):
  if texture_path is None:
    mesh = o3d.io.read_triangle_mesh(path)
  else:
    mesh = o3d.io.read_triangle_mesh(path, True)
    mesh.textures = [o3d.io.read_image(texture_path)]

  return mesh

# merge 2 meshes into 1
def combine(meshA, meshB): return meshA + meshB

# move the mesh along a given direction
def translate(mesh, shift=[0, 0, 0]):
  vertices = np.asarray(mesh.vertices)
  vertices += np.array(shift)

# scale along the center
def scale(mesh, scale=[1, 1, 1]):
  vertices = np.asarray(mesh.vertices)
  center = np.mean(vertices, axis=0)

  vertices -= center
  vertices *= scale
  vertices += center

# rotate along the center
def rotate(mesh, theta=0, axis='x'):
  vertices = np.asarray(mesh.vertices)
  center = np.mean(vertices, axis=0)

  # define rotation matrix
  if axis == 'x': 
    m = np.array([
      [ 1,              0,              0],
      [ 0,  np.cos(theta), -np.sin(theta)],
      [ 0,  np.sin(theta),  np.cos(theta)]
    ])
  elif axis == 'y':
    m = np.array([
      [ np.cos(theta), 0, np.sin(theta)],
      [             0, 1,             0],
      [-np.sin(theta), 0, np.cos(theta)]
    ])
  elif axis == 'z':
    m = np.array([
      [np.cos(theta), -np.sin(theta), 0],
      [np.sin(theta),  np.cos(theta), 0],
      [            0,              0, 1]
    ])
  else: return

  vertices -= center
  vertices = np.dot(vertices, m.T)
  vertices += center

  mesh.vertices = o3d.utility.Vector3dVector(vertices)

if __name__ == "__main__":
  # meshA = load_obj("../lesson1/6-cube.obj", "../lesson1/grass.png")
  meshA = load_obj("../lesson1/3-quad.obj", "../lesson1/grass.png")
  meshB = copy.deepcopy(meshA)

  # rotate(mesh, np.pi/4, 'x')
  # mesh.compute_triangle_normals()
  # meshB.compute_triangle_normals()
  # rotate(meshA, np.pi/4, 'x')

  print(np.asarray(meshA.triangle_normals))
  print(np.asarray(meshA.vertex_normals))

  if not meshA.triangle_normals: print('wefjiefjiewj')

  # meshA.compute_triangle_normals()
  meshA.compute_vertex_normals()

  print(np.asarray(meshA.triangle_normals))
  print(np.asarray(meshA.vertex_normals))

  meshA.triangle_normals = o3d.utility.Vector3dVector([])

  # save obj
  o3d.io.write_triangle_mesh("./output/output.obj", meshA)

