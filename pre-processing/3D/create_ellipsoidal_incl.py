import numpy as np
file_ellipsoids = open("../../meshes/txt_mesh/ellipsoid_gmsh","w") 
box_len = 1
class ellipsoid:
    """
    ellipsoids in 3-D
        Args:
            xx: x-coordinate of the center of the ellipsoid
            yy: y-coordinate of the center of the ellipsoid
            zz: z-coordinate of the center of the ellipsoid
            exx: aspect ratio in direction xx
            eyy: aspect ratio in direction yy
            ezz: aspect ratio in direction zz
    """
    def __init__(self,xx,yy,zz,rr,exx,eyy,ezz):
        self.x = xx
        self.y = yy
        self.z = zz
        self.r = rr
        self.ex = exx
        self.ey = eyy
        self.ez = ezz

def create_dataset(r,exx,eyy,ezz,x,y,z):
    """
    Dataset with geometric information 
    Args:
        r: radius of the ellipsoids
        exx: aspect ratio in direction xx
        eyy: aspect ratio in direction yy
        ezz: aspect ratio in direction zz
        x: list with the x coordinates of the different center of the ellipsoids
        y: list with th  y coordinates of the different center of the ellipsoids
        z: list with th  z coordinates of the different center of the ellipsoids
    Writes:
        writes the geometrical information for the semi-automatic solution
    """
    #c is a counter to use when giving a tag to the geometries
    c=0
    #ell will have all the ellipsoids appended
    ell = []
    #itarating through the coordinates
    for k in (z):#looping over all ellipsoids
        for i in (x):
            for j in (y):
                e = ellipsoid(i,j,k,r,exx,eyy,ezz)
                ell.append(e)
                #First create a sphere 
                file_ellipsoids.write("Sphere({}) = {{x+{}, y+{}, z+{}, {}}}; \n".format(c+2,e.x,e.y,e.z,e.r))
                #Dilate the sphere to make it an ellipsoid
                file_ellipsoids.write("Dilate {{{{ x+{}, y+{}, z+{}}},{{{},{},{}}}}} {{Volume{{{}}}; }} \n".format(e.x,e.y,e.z,e.ex,e.ey,e.ez,c+2))
                c+=1
    file_ellipsoids.write("v() = BooleanFragments {{ Volume{{{}}}; Delete; }}{{ Volume{{{}}}; Delete; }}; \n".format(1,"2 :"+str(len(ell)+1)))
    return ell

def set_physical_regions(ell):
    """
    Set the phases of the material if not intersecting
    Args:
        rad: list with the radius
    Writes:
        writes the physical information
    """
    #finds the tags of the second phase
    ellipsoid_indices = list(range(2,len(ell)+2))
    file_ellipsoids.write("Physical Volume({}) = {{{}}}; \n".format(1,len(ell)+2))
    file_ellipsoids.write("Physical Volume({}) = {{{}}}; \n".format(2,str(ellipsoid_indices)[1:-1]))
    
def set_resolution(lmin,lmax):
    """
    Set the resolution
    Args:
        lmin: minimum length of the mesh if using semi-automatic solution with Gmsh
        lmax: maximum length of the mesh if using semi-automatic solution with Gmsh
    Writes:
        writes the lmin,lmax
    """
    file_ellipsoids.write("Mesh.CharacteristicLengthMin = {}; \n".format(lmin))
    file_ellipsoids.write("Mesh.CharacteristicLengthMax = {}; \n".format(lmax))


#------------------------------------------------
#locations for oblate spheroids (r = 0.04,exx=1,eyy=10,ezz=10)
#x = [0.25,0.75]
#y = [0.25,0.75]
#z = [0.25,0.75]
#-------------------------------------------------
##locations for plorate spheroids (r = 0.05,exx=1,eyy=1,ezz=8)
#x = [0.1,0.3,0.5,0.7,0.9]
#y = [0.1,0.3,0.5,0.7,0.9]
#z = [0.5]
##2nd example (r = 0.05,exx=1,eyy=1,ezz=4)
x = [0.25,0.75]
y = [0.25,0.75]
z = [0.25,0.75]
#-------------------------------------------------
ell = create_dataset(r = 0.05,exx=1,eyy=1,ezz=4,x=x,y=y,z=z)
set_physical_regions(ell)
#make sure not to put resolution bigger than a radius
set_resolution(0.03,0.03)
file_ellipsoids.close()