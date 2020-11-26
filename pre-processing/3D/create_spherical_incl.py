import random
import numpy as np

file_spheres = open("../../meshes/txt_mesh/spherical_gmsh","w") 
box_len = 1


class sphere:
    """
    Sphere in 3-D
        Args:
            xx: x-coordinate of the center of the sphere
            yy: y-coordinate of the center of the sphere
            zz: z-coordinate of the center of the sphere            
            rr: radius of the circle
    """
    def __init__(self,xx,yy,zz,rr):
        self.x = xx
        self.y = yy
        self.z = zz
        self.r = rr

def random_sphere(r):
    '''
    random sphere with radius r
        Args:
            r: radius of the sphere
            inside: defines if the circles can cross the boundaries or not
        Return:
            a random sphere
    '''
    x = random.uniform(r, box_len-r)
    y = random.uniform(r, box_len-r)
    z = random.uniform(r, box_len-r)
    return sphere(x,y,z,r)

def intersect(s,spheres,perc_intersect=1.):
    '''
    test if the circles intersect
        Args:
            c: current circle
            circles: list of the previous circles
            perc_intersect: how much of the spheres can intersect in terms of distance. valid values[1 to 1.5], 1:not intersecting
        Return:
            True for intersecting/or more than allowed interesect and False for not intersecting/or allowed intersect 
    '''
    for sphere in spheres:
        dist = np.sqrt(((s.x - sphere.x)*perc_intersect)**2 + ((s.y - sphere.y)*perc_intersect)**2 + ((s.z - sphere.z)*perc_intersect)**2)
        if dist < s.r + sphere.r:#Tests if the distance of the centers are bigger than the minimum allowed
            return True
    return False

def create_dataset(n_spheres,r,perc_intersect=1.):
    """
    Dataset with the geometric information
    Args:
        name:name of the geometry
        n_spheres: number of spheres 
        r:list with the radius of the spheres
        perc_intersect = how much of the spheres can intersect in terms of distance. valid values[1 to 1.5], 1:not intersecting
    Writes:
        writes the geometrical information for the semi-automatic solution
    """
    spheres = []
    spheres_arr = np.zeros((n_spheres,4))
    for i in range (n_spheres):
        s = random_sphere(r[i])#creates a random sphere of r[i] inside the cubic domain
        j=0
        while intersect(s,spheres,perc_intersect) == True: #Give a perc_intersect bigger than 1 to allow intersection
            s = random_sphere(r[i]) #random sphere inside the domain
            j+=1
            if (j%500000)==0:
                print(j,r[i]) #this is just a test to see if it will go in an infinite loop (by giving large porosity)
        spheres.append(s)
        spheres_arr[i,:] = (s.x,s.y,s.z,s.r)
        file_spheres.write("Sphere({}) = {{x+{}, y+{}, z+{}, {}}}; \n".format(i+2,s.x,s.y,s.z,s.r))
    file_spheres.write("v() = BooleanFragments {{ Volume{{{}}}; Delete; }}{{ Volume{{{}}}; Delete; }}; \n".format(1,"2 :"+str(len(spheres_arr)+1)))
    return spheres_arr

def get_parameters(porosity,min_r,max_r):
    '''
    returns the radius between min_r and
    max_r until it apporaches the desired porosity
        Args:
        porosity: desired volume fraction
        min_r: minimum radius for the spheres
        max_r: maximum radius for the spheres
    Returns:
        list with radius of spheres'''
    vol_pores = porosity*box_len**3 #volume vox*porosity
    left_volume = vol_pores
    tol = 0.01
    max_r_possible = ((3*left_volume) / (4*np.pi))**(1/3) #by the spherical volume equation
    rad = [] #will contain all radius
    while left_volume > tol:
        if min_r > max_r_possible: #test if the min_r given by the user is larger than the max_r_possible
            r = max_r_possible
        else:
            r = random.uniform(min_r,max_r) #takes a random radius from the bounds
        vol_taken = (4*np.pi*r**3)/3 #this is the volume by the one sphere
        left_volume -= vol_taken 
        max_r_possible = ((3*left_volume) / (4*np.pi))**(1/3)
        if max_r > max_r_possible:
            max_r = max_r_possible
        rad.append(r)
    return rad

def get_single_sphere(porosity):
    '''
    returns the radius for a single sphere to approximate the porosity
        Args:
        porosity: desired volume fraction
    Returns:
        list with single radius'''
    return [((3*porosity)/(4*np.pi))**(1/3)]
    
def set_physical_regions(rad):
    """
    Set the phases of the material if not intersecting
    Args:
        rad: list with the radius
    Writes:
        writes the physical information
    """
    spheres_indices = list(range(2,len(rad)+2))
    file_spheres.write("Physical Volume({}) = {{{}}}; \n".format(1,len(rad)+2))
    file_spheres.write("Physical Volume({}) = {{{}}}; \n".format(2,str(spheres_indices)[1:-1]))
    
def set_resolution(lmin,lmax):
    """
    Set the resolution
    Args:
        lmin: minimum length of the mesh if using semi-automatic solution with Gmsh
        lmax: maximum length of the mesh if using semi-automatic solution with Gmsh
    Writes:
        writes the lmin,lmax
    """
    file_spheres.write("Mesh.CharacteristicLengthMin = {}; \n".format(lmin))
    file_spheres.write("Mesh.CharacteristicLengthMax = {}; \n".format(lmax))


#rad = get_single_sphere(0.15)

##It is very important to sort the radius of the spheres to be able to archieve higher porosities up to 47%
rad = sorted(get_parameters(0.3,0.09,0.12),reverse=True)  
spheres = create_dataset(len(rad),rad)
set_physical_regions(rad)
set_resolution(0.07,0.07)
file_spheres.close()

