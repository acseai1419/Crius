import random
import numpy as np

square_len = 1
class circle:
    """
    circle in 2-D
        Args:
            xx: x-coordinate of the center of the circle
            yy: y-coordinate of the center of th cirlce
            rr: radius of the circle
    """
    def __init__(self,xx,yy,rr):
        self.x = xx
        self.y = yy
        self.r = rr

def random_circle(r,inside = True):
    '''
    random circle with radius r
        Args:
            r: the radius of the circle
            inside: defines if the circles can cross the boundaries or not (False is also supported)
        if inside = False follow the notebook in meshes/gmsh for intersected spherical inclusions(semi-automati tagging)
        Return:
            a random circle
    '''
    if inside == True: #not crossing boundaries
        x = random.uniform(r, square_len-r)
        y = random.uniform(r, square_len-r)
        return circle(x,y,r)
    else: #inclusions can cross boundaries
        x = random.uniform(0,square_len)
        y = random.uniform(0,square_len)
        x_p = x
        y_p = y
        i_p = 0 #i_p shows how many boundaries the surface is crossing
        if (x<r): #left boundary
            x_p = x + square_len
            i_p+=1
        elif (x>square_len-r):#right boundary
            x_p = x - square_len
            i_p+=1
        if (y<r): #bottom boundary
            y_p = y + square_len
            i_p+=1
        elif (y>square_len-r): #top boundary
            y_p = y - square_len
            i_p+=1
        if i_p == 0 : #not crossing boundaries
            return circle(x,y,r),None,None,None,i_p
        elif i_p == 1: #crossing one boundary
            return circle(x,y,r),circle(x_p,y_p,r),None,None,i_p
        return circle(x,y,r),circle(x_p,y_p,r),circle(x,y_p,r),circle(x_p,y,r),i_p #in a corner crossing two boundaries

def intersect(c,circles):
    '''
    test if the circles intersect
        Args:
            c: current circle
            circles: list of the previous circles
        Return:
            True for intersecting and False for not intersecting
    '''
    for circle in circles:
        dist = np.sqrt((c.x - circle.x)**2 + (c.y - circle.y)**2) #distance of the centers of the two circles
        if dist < c.r + circle.r:
            return True
    return False

def create_dataset(name,n_circles,r,lmin = 0.05,lmax = 0.05,inside = True,meshes_location="./meshes"):
    """
    Dataset with the geometric information
    Args:
        name:name of the geometry
        n_circles: number of circles 
        r:list with the radius of the circles
        lmin: minimum length of the mesh if using semi-automatic solution with Gmsh
        lmax: maximum length of the mesh if using semi-automatic solution with Gmsh
        inside: boolean defining if the circles can cross the boundaries
        meshes_location: the location of the mesh in regard with where you are running the code
    Returns:
        an array with the information of the layers for the mshr library
    Writes:
        writes the geometrical and physical information for the semi-automatic solution with Gmsh
    """
    circles = []
    circles_arr = np.zeros((n_circles,3))
    file_circles = open(meshes_location+"/txt_mesh/gmsh_circular","w") #file for Gmsh semi automatic
    if inside:#if not intersecting boundaries
        for i in range (n_circles): #this will let us go though each circle
            c = random_circle(r[i]) #random circle of r[i]
            while intersect(c,circles) == True: #when they are not intersect it can continue
                c = random_circle(r[i])
            circles.append(c) #appending the valid circle
            circles_arr[i,:] = (c.x,c.y,c.r)
            file_circles.write("Disk({}) = {{x+{}, y+{}, z+{}, {}}}; \n".format(i+2,c.x,c.y,0.,c.r)) #geometric info for gmsh
        file_circles.write("s() = BooleanFragments {{ Surface{{{}}}; Delete; }}{{ Surface{{{}}}; Delete; }}; \n".format(1,"2 :"+str(len(circles_arr)+1)))#surface substraction for gmsh
        set_physical_regions(r,file_circles) #marks the inclusions with phase 1 and the rest with phase 0 in Gmsh
        set_resolution(lmin,lmax,file_circles) #resolution for Gmsh software
        np.savetxt(meshes_location+"/txt_mesh/"+name+".txt", circles_arr) #This is for the mshr library - geometric information
        file_circles.close()
        return circles_arr
    else:#if can cross boundaries !This can only run correctly with Gmsh semi-automatic solution! Mshr library does not support periodic boundaries
        j=0
        circles_arr = np.zeros((n_circles,3))
        for i in range (n_circles):
            c,c_p1,c_p2,c_p3,i_p = random_circle(r[i],False)
            print(c.x,c.y,c.r)
            while intersect(c,circles) == True:
                c,c_p1,c_p2,c_p3,i_p  = random_circle(r[i],False)
            j+=1
            circles.append(c)
            circles_arr[i,:] = (c.x,c.y,c.r) 
            file_circles.write("Disk({}) = {{x+{}, y+{}, z+{}, {}}}; \n".format(j+1,c.x,c.y,0.,c.r)) #saving the first circle (always exist)
            if i_p == 1: #crossing one boundary
                j+=1
                circles.append(c_p1)
                circles_arr = np.vstack((circles_arr,[c_p1.x,c_p1.y,c_p1.r]))
                file_circles.write("Disk({}) = {{x+{}, y+{}, z+{}, {}}}; \n".format(j+1,c_p1.x,c_p1.y,0.,c_p1.r)) #if crossing one boundary saving second circle
            elif i_p == 2: #crossing boundaries on a corner 
                j+=1
                circles.append(c_p1)
                circles_arr = np.vstack((circles_arr,[c_p1.x,c_p1.y,c_p1.r]))
                file_circles.write("Disk({}) = {{x+{}, y+{}, z+{}, {}}}; \n".format(j+1,c_p1.x,c_p1.y,0.,c_p1.r)) #if on corner all 4 circles are saved
                j+=1
                circles.append(c_p2)
                circles_arr = np.vstack((circles_arr,[c_p2.x,c_p2.y,c_p2.r]))
                file_circles.write("Disk({}) = {{x+{}, y+{}, z+{}, {}}}; \n".format(j+1,c_p2.x,c_p2.y,0.,c_p2.r)) #if on corner all 4 circles are saved
                j+=1
                circles.append(c_p3)
                circles_arr = np.vstack((circles_arr,[c_p3.x,c_p3.y,c_p3.r]))
                file_circles.write("Disk({}) = {{x+{}, y+{}, z+{}, {}}}; \n".format(j+1,c_p3.x,c_p3.y,0.,c_p3.r)) #if on corner all 4 circles are saved
        file_circles.write("s() = BooleanFragments {{ Surface{{{}}}; Delete; }}{{ Surface{{{}}}; Delete; }}; \n".format(1,"2 :"+str(len(circles_arr)+1)))
        set_physical_regions(r,file_circles)
        set_resolution(lmin,lmax,file_circles)
        np.savetxt(meshes_location+"/txt_mesh/"+name+".txt", circles_arr) 
        file_circles.close()
        return circles_arr

def get_parameters(porosity,min_r,max_r):
    '''
    returns the radius between min_r and
    max_r until it apporaches the desired porosity
        Args:
        porosity: desired volume fraction
        min_r: minimum radius for the circles
        max_r: maximum radius for the circles
    Returns:
        list with radius of circles'''
    vol_pores = porosity*square_len**2 #initail volume taken by the inclusions
    left_volume = vol_pores 
    tol = 0.01 
    max_r_possible = np.sqrt(left_volume/np.pi) #max radius for reaching the left volume
    rad = [] #list with all the radius until reaching the desired porosity
    while left_volume > tol:
        if min_r > max_r_possible:
            r = max_r_possible
        else:
            r = random.uniform(min_r,max_r)
        vol_taken = np.pi*r**2 
        left_volume -= vol_taken #substracts the inclusion volume from the left
        max_r_possible = np.sqrt(left_volume/np.pi)
        if max_r > max_r_possible:
            max_r = max_r_possible
        rad.append(r)
    return rad

def set_physical_regions(rad,file_circles):
    """
    Set the phases of the material if using semi-automatic solution Gmsh
    Args:
        rad: list with the radius
        file_circles: the file in meshes/txt_mesh for writhing the information of the semi automatic solution 
    Writes:
        writes the physical information for the semi-automatic solution
    """
    circles_indices = list(range(2,len(rad)+2))
    file_circles.write("Physical Surface({}) = {{{}}}; \n".format(0,len(rad)+2))
    file_circles.write("Physical Surface({}) = {{{}}}; \n".format(1,str(circles_indices)[1:-1]))
def set_resolution(lmin,lmax,file_circles):
    """
    Set the resolution if using semi-automatic solution Gmsh
    Args:
        lmin: minimum length of the mesh if using semi-automatic solution with Gmsh
        lmax: maximum length of the mesh if using semi-automatic solution with Gmsh
        file_circles: the file in meshes/txt_mesh for writhing the information of the semi automatic solution 
    Writes:
        writes the lmin,lmax
    """
    file_circles.write("Mesh.CharacteristicLengthMin = {}; \n".format(lmin)) #this will be the min length for the 2-D mesh in Gmsh!
    file_circles.write("Mesh.CharacteristicLengthMax = {}; \n".format(lmax)) #this will be the max length for the 2-D mesh in Gmsh!