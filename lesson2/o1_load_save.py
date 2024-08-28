import numpy as np
import open3d as o3d

# load obj
def load_obj(path, texture_path=None):
  if texture_path is None:
    mesh = o3d.io.read_triangle_mesh(path)
  else:
    mesh = o3d.io.read_triangle_mesh(path, True)
    mesh.textures = [o3d.io.read_image(texture_path)]

  vertices = np.asarray(mesh.vertices)
  normals = np.asarray(mesh.vertex_normals)
  triangles = np.asarray(mesh.triangles)
  uvs = np.asarray(mesh.triangle_uvs).reshape(-1, 3, 2)

  print('vertices ', vertices.shape, '\n', vertices, end="\n\n")
  print('normals ', normals.shape, '\n', normals, end="\n\n")
  print('faces ', triangles.shape, '\n', triangles, end="\n\n")
  print('uvs ', uvs.shape, '\n', uvs, end="\n\n")

  return mesh

if __name__ == "__main__":
  mesh = load_obj("../lesson1/1_triangle.obj")
  # mesh = load_obj("../lesson1/2_quad.obj")
  # mesh = load_obj("../lesson1/3_quad.obj", "../lesson1/dirt.png")
  # mesh = load_obj("../lesson1/4_quad.obj", "../lesson1/dirt.png")
  # mesh = load_obj("../lesson1/5_edge.obj", "../lesson1/grass.png")
  # mesh = load_obj("../lesson1/6_cube.obj", "../lesson1/grass.png")

  # save obj
  o3d.io.write_triangle_mesh("./output/output.obj", mesh)

