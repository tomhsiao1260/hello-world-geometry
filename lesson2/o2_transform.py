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

# merge meshes into 1
def combine(meshes, share_texture=False):
  ref_mesh = meshes[0]
  combine_mesh = copy.deepcopy(ref_mesh)

  # combine
  for mesh in meshes[1:]: combine_mesh += mesh

  if share_texture:
    # share textures
    combine_mesh.textures = ref_mesh.textures
    # share material ids
    ids = ref_mesh.triangle_material_ids
    ids = np.tile(np.asarray(ids), len(meshes))
    ids = o3d.utility.IntVector(ids)
    combine_mesh.triangle_material_ids = ids

  return combine_mesh

# update normals
def compute_normals(mesh):
  if not mesh.triangle_normals:
    mesh.compute_vertex_normals()
    mesh.triangle_normals = o3d.utility.Vector3dVector([])
  else:
    mesh.compute_vertex_normals()
    mesh.compute_triangle_normals()

if __name__ == "__main__":
  meshA = load_obj("../lesson1/6_cube.obj", "../lesson1/grass.png")
  meshB = copy.deepcopy(meshA)

  translate(meshA, [ 1, 0, 0])
  translate(meshB, [-1, 0, 0])

  scale(meshB, [0.5, 0.5, 0.5])
  scale(meshB, [1.5, 1.5, 1.5])

  rotate(meshA, np.pi/4, 'x')
  rotate(meshB, np.pi/4, 'z')

  mesh = combine([meshA, meshB], True)
  compute_normals(mesh)

  # save obj
  o3d.io.write_triangle_mesh("./output/output.obj", mesh)

