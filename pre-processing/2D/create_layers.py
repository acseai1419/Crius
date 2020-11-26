import numpy as np
from create_mesh import *

square_len = 1
class layer:
    """
    layer in 2-D
        Args:
            xx: x-coordinate of the center of the layer
            dd: width of the layer
    """
    def __init__(self,xx,dd):
        self.x = xx
        self.left = xx - dd/2 #left x coordinate of the layer
        self.right = xx + dd/2 #rifht x coordinate of the layer
        self.d = dd

def create_dataset(x=[0.1,0.3,0.5,0.7,0.9],d = 0.1,lmin=0.07,lmax=0.07,meshes_location="./meshes"):
    """
    Dataset with geometric information
    Args:
        x: list with the x coordinates of the center of the layers
        d: width of layer
        lmin: minimum length of the mesh if using semi-automatic solution with Gmsh
        lmax: maximum length of the mesh if using semi-automatic solution with Gmsh
        meshes_location: the location of the mesh in regard with where you are running the code
    Returns:
        an array with the information of the layers for the mshr library
    Writes:
        writes the geometrical and physical information for the semi-automatic solution
    """
    layers_arr = np.zeros((len(x),2)) #containing the information of all the layers
    file_layers = open(meshes_location+"/txt_mesh/gmsh_layers","w") #file for the semi-automatic solution with gmsh
    for i in range (len(x)):
        l = layer(x[i],d) 
        layers_arr[i,:] = (l.left,l.right) #the layers array for Mshr needs the left and right coordinate of the rectangle to define the geometry
        file_layers.write("Rectangle({}) = {{x+{}, y+{}, z+{}, {},{}}}; \n".format(i+2,l.left,0,0.,l.d,1)) #geometric information gmshr
        np.savetxt(meshes_location+"/txt_mesh/layers.txt", layers_arr) 
    file_layers.write("s() = BooleanFragments {{ Surface{{{}}}; Delete; }}{{ Surface{{{}}}; Delete; }}; \n".format(1,"2 :"+str(len(x)+1))) #surface substractin gmsh
    set_physical_regions(x,file_layers) #set the two physical regions
    set_resolution(lmin,lmax,file_layers) #resolution for gmsh software! not the same for mshr
    file_layers.close()
    return layers_arr

def set_physical_regions(x,file_layers):
    """
    Set the phases of the material if using semi-automatic solution Gmsh
    Args:
        x: list with the x coordinates of the center of the layers
        file_layers: the file in meshes/txt_mesh for writhing the information of the semi automatic solution 
    Writes:
        writes the physical information for the semi-automatic solution in layers
    """
    second_phase_indices = np.array(range(2,len(x)+2))
    first_phase_indices = second_phase_indices + len(x)
    first_phase_indices = np.append(first_phase_indices,first_phase_indices[-1]+1)
    second_phase_indices = list(second_phase_indices)
    first_phase_indices = list(first_phase_indices)
    file_layers.write("Physical Surface({}) = {{{}}}; \n".format(0,str(first_phase_indices)[1:-1]))
    file_layers.write("Physical Surface({}) = {{{}}}; \n".format(1,str(second_phase_indices)[1:-1]))

def set_resolution(lmin,lmax,file_layers):
    """
    Set the resolution if using semi-automatic solution Gmsh
    Args:
        lmin: minimum length of the mesh if using semi-automatic solution with Gmsh
        lmax: maximum length of the mesh if using semi-automatic solution with Gmsh
        file_layers: the file in meshes/txt_mesh for writhing the information of the semi automatic solution 
    Writes:
        writes the lmin,lmax
    """
    file_layers.write("Mesh.CharacteristicLengthMin = {}; \n".format(lmin)) #this will be the min length for the 2-D mesh in Gmsh!
    file_layers.write("Mesh.CharacteristicLengthMax = {}; \n".format(lmax)) #this will be the max length for the 2-D mesh in Gmsh!