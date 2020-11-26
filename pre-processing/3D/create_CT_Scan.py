import numpy as np
import random
file_voxels = open("../../meshes/txt_mesh/ct_scan_gmsh","w") 
box_len = 1
class voxel:
    """
    Voxel in 3-D
        Args:
            xx: x-coordinate of the center of the cube
            yy: y-coordinate of the center of the cube
            zz: z-coordinate of the center of the cube
            ee: length of the cube
    """    
    def __init__(self,xx,yy,zz,ee):
        self.x = xx
        self.y = yy
        self.z = zz
        self.e = ee
            
def create_dataset(resolution):
    """
    Dataset with geometric information 
    Args:
        resolution here is the resolution of the CT image NOT the mesh resolution (how many voxels are in the image)
    Writes:
        writes the geometrical information for the semi-automatic solution
    Return:
        length of boxes
    """
    assert resolution**(1/3).is_integer() == True #asserts that the resolution of the CT scan has an intiger cubic root
    length = box_len / resolution**(1/3) #length of the voxels are the box length devided by the voxels in one of the directions
    z = 0 #starting fro (0,0,0)
    c = 2 #counter to be used when writing the geometric tags
    for k in range (round(resolution**(1/3))): #loops over all voxels
        y = 0
        for j in range (round(resolution**(1/3))):
            x = 0
            for i in range (round(resolution**(1/3))):
                v = voxel(x,y,z,length)#creates the voxel
                file_voxels.write("Box({}) = {{{}, {}, {}, {}, {}, {}}}; \n".format(c,v.x,v.y,v.z,v.e,v.e,v.e)) #write the geometric info
                x+=length
                c+=1
            y+=length
        z+=length
    file_voxels.write("v() = BooleanFragments {{ Volume{{{}}}; Delete; }}{{ Volume{{{}}}; Delete; }}; \n".format(1,"2 :"+str(resolution+1)))#substracts voxels from the cubic domain
    return length

def set_physical_regions(n_regions,resolution):
    """
    Set the phases of the material if not intersecting
    Args:
        n_regions: number of regions
        resolution: resolution of the CT scan
    Writes:
        writes the physical information of the n phases
    """
    assert n_regions < resolution #regions cannot be more than the voxels
    phases = np.zeros(resolution) 
    for i in range (resolution):
        phase = random.randint(0,n_regions-1) #random alocation of phases
        phases[i] = phase
    for i in range(n_regions):
        indices = np.where(phases == i)
        indices = (indices+np.full_like(indices,2)).tolist()
        s_indices = str(indices)
        file_voxels.write("Physical Volume({}) = {{{}}}; \n".format(i+1,s_indices[2:-2]))    
    

length = create_dataset(27)#input in length, the cubic root of the resolution should be an integer(e.g. 8,27,84,..)
set_physical_regions(4,27) #three phases, resolution: 8 boxes
#here the resolution of the mesh is characterized by the resolution of the CT scan
file_voxels.write("Mesh.CharacteristicLengthMin = {}; \nMesh.CharacteristicLengthMax = {};".format(length,length))
file_voxels.close()



