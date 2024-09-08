import copy
import numpy as np
import open3d as o3d

from o2_transform import translate, scale, rotate
from o2_transform import load_obj, combine, compute_normals

def generate_cube_rod(cube, rod):
  translate(cube, [-0.5, -0.5, -0.5])
  rotate(cube, -np.pi/2, 'z')

  translate(rod, [-0.5, -0.5, 0])
  scale(rod, [2, 0.2, 1])
  translate(rod, [-2/2, 0, 0])

  return combine([cube, rod])

def generate_cube_rod_pair(cube_rod):
  cube_rod_A = copy.deepcopy(cube_rod)
  cube_rod_B = copy.deepcopy(cube_rod)

  rotate(cube_rod_B, np.pi, 'y')
  translate(cube_rod_A, [ 2, 0, 0])
  translate(cube_rod_B, [-2, 0, 0])

  return combine([cube_rod_A, cube_rod_B], True)

def generate_double_helix(cube_rod_pair):
  cube_rod_pair_list = []

  for i in range(30):
    shift = i * 1
    angle = i * np.pi / 10
    temp_cube_rod_pair = copy.deepcopy(cube_rod_pair)

    rotate(temp_cube_rod_pair, angle, 'y')
    translate(temp_cube_rod_pair, [0, shift, 0])
    cube_rod_pair_list.append(temp_cube_rod_pair)

  return combine(cube_rod_pair_list, True)

if __name__ == "__main__":
  rod = load_obj("../lesson1/4_quad.obj", "../lesson1/dirt.png")
  cube = load_obj("../lesson1/6_cube.obj", "../lesson1/grass.png")

  cube_rod = generate_cube_rod(cube, rod)
  cube_rod_pair = generate_cube_rod_pair(cube_rod)

  # calculate normals & save model
  compute_normals(cube_rod_pair)
  o3d.io.write_triangle_mesh("./output/cube_rod_pair.obj", cube_rod_pair)

  double_helix = generate_double_helix(cube_rod_pair)

  # calculate normals & save model
  compute_normals(double_helix)
  o3d.io.write_triangle_mesh("./output/double_helix.obj", double_helix)

 