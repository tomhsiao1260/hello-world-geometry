# https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.Delaunay.html

import open3d as o3d
import numpy as np
from scipy.spatial import Delaunay

def create_random_sphere_points(num_points=100, radius=1.0):
    # Generate random points on a sphere surface
    phi = np.random.uniform(0, np.pi, num_points)
    theta = np.random.uniform(0, np.pi / 2, num_points)

    x = radius * np.sin(theta) * np.cos(phi)
    y = radius * np.sin(theta) * np.sin(phi)
    z = radius * np.cos(theta)
    
    points_3d = np.vstack((x, y, z)).T
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(points_3d)
    
    # Store UV coordinates for 2D triangulation
    uv_coords = np.column_stack((phi / np.pi, -theta / (np.pi/2)))
    
    return points_3d, uv_coords, pcd

def delaunay_reconstruction(points_3d, uv_coords):
    # Perform Delaunay triangulation on 2D UV coordinates
    tri = Delaunay(uv_coords)
    
    # Create Open3D TriangleMesh using 3D points and 2D triangulation indices
    mesh = o3d.geometry.TriangleMesh()
    mesh.vertices = o3d.utility.Vector3dVector(points_3d)
    mesh.triangles = o3d.utility.Vector3iVector(tri.simplices)

    compute_normals(mesh)
    
    return mesh

# update normals
def compute_normals(mesh):
  if not mesh.triangle_normals:
    mesh.compute_vertex_normals()
    mesh.triangle_normals = o3d.utility.Vector3dVector([])
  else:
    mesh.compute_vertex_normals()
    mesh.compute_triangle_normals()

def main():
    # Generate point cloud with 100 random points and their UV coordinates
    points_3d, uv_coords, pcd = create_random_sphere_points(num_points=1000, radius=1.0)
    
    # Perform Delaunay triangulation reconstruction using UV coordinates
    mesh = delaunay_reconstruction(points_3d, uv_coords)
    
    # Visualize the point cloud and reconstructed mesh
    o3d.visualization.draw_geometries([pcd, mesh], window_name="Delaunay UV Sphere")
    
    # Save the mesh as an OBJ file (todo: cannot save uv coords)
    output_path = "./output/sphere.obj"
    o3d.io.write_triangle_mesh(output_path, mesh)

if __name__ == "__main__":
    main()
