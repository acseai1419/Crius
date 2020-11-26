import numpy as np
file_layers = open("../../meshes/txt_mesh/layers3D_gmsh","w") 
box_len = 1
class layer:
    """
    layer in 3-D
        Args:
            xx: x-coordinate of the center of the layer
            dd: width of the layer
    """
    def __init__(self,xx,dd):
        self.x = xx
        self.left = xx - dd/2
        self.right = xx + dd/2
        self.d = dd

def create_dataset(x=[0.1,0.3,0.5,0.7,0.9],d = 0.1):
    """
    Dataset with geometric information 
    Args:
        x: list with the x coordinates of the center of the layers
        d: width of layer
    Writes:
        writes the geometrical information for the semi-automatic solution
    """
    for i in range (len(x)):
        l = layer(x[i],d)
        file_layers.write("Box({}) = {{x+{}, y, z, {}, {}, {} }}; \n".format(i+2,l.left,l.d,box_len,box_len))
    file_layers.write("v() = BooleanFragments {{ Volume{{{}}}; Delete; }}{{ Volume{{{}}}; Delete; }}; \n".format(1,"2 :"+str(len(x)+1)))
    return 0

def set_physical_regions(x=[0.1,0.3,0.5,0.7,0.9]):
    """
    Set the phases of the material
    Args:
        x: list with the x coordinates of the center of the layers
    Writes:
        writes the physical information
    """
    phase2_indices = list(range(2,len(x)+2))
    phase1_indices = list(range(len(x)+2,len(x)+1+len(x)+2))
    file_layers.write("Physical Volume({}) = {{{}}}; \n".format(1,str(phase1_indices)[1:-1]))
    file_layers.write("Physical Volume({}) = {{{}}}; \n".format(2,str(phase2_indices)[1:-1]))
def set_resolution(lmin,lmax):
    """
    Set the resolution if using semi-automatic solution Gmsh
    Args:
        lmin: minimum length of the mesh if using semi-automatic solution with Gmsh
        lmax: maximum length of the mesh if using semi-automatic solution with Gmsh
        file_layers: the file in meshes/txt_mesh for writhing the information of the semi automatic solution 
    Writes:
        writes the lmin,lmax
    """
    file_layers.write("Mesh.CharacteristicLengthMin = {}; \n".format(lmin))
    file_layers.write("Mesh.CharacteristicLengthMax = {}; \n".format(lmax))
    
create_dataset(d = 0.10)
set_physical_regions()
set_resolution(0.25,0.25)
file_layers.close()