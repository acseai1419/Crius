from dolfin import *

def save_mesh_mpi(name,meshes_location="../meshes",mesh_location="/gmsh/"):
    """
    Saves the mesh in .h5 to be read from mpi 
    Args:
        name
    """
    mesh = Mesh(meshes_location+ mesh_location+ name + ".xml")
    subdomains = MeshFunction("size_t", mesh, meshes_location + mesh_location + name + "_physical_region.xml")
    hdf = HDF5File(mesh.mpi_comm(), meshes_location + "/mpi_mesh/file.h5", "w")
    hdf.write(mesh, "/mesh")
    hdf.write(subdomains, "/subdomains")
    
save_mesh_mpi("half_ellips_02")
