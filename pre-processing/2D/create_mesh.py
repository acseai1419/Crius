import numpy as np
from fenics import *
import mshr

def create_mesh_2D(name,resolution,inclusions=None,meshes_location="./meshes"):
    '''
    creates the mesh for the two types of geometries with mshr libray (layered,circular inclusions)
        Args:
        name: name of file with mshr informatiion
        resolution: resolution of the mesh in mshr
        inclusions = inclusions can be imported from the file with mshr info or given as an argument in a numpy array (contains geometric information)
    Returns:
        the mesh and the subdomains of the geometry
    '''
    if type(inclusions)!= np.array: #if not given as argument it reads the array from the text file 
        inclusions = np.genfromtxt(meshes_location+"/txt_mesh/"+ name + ".txt", dtype=float)
    if(name[0:19] == "circular_inclusions"): 
        domain = mshr.Rectangle(Point(0., 0.), Point(1., 1.)) #this is the domain
        for i, (x, y, r) in enumerate(inclusions): #going throug the circular inclusions
            circle = mshr.Circle(Point(x, y), r) #creating a circle geometry with the geometric information
            domain.set_subdomain(i + 1, circle) #marks inclusions with domain larger than zero
    elif (name == "layers"):
        domain = mshr.Rectangle(Point(0., 0.), Point(1., 1.)) #initial domain
        for i, (left,right) in enumerate(inclusions): #going through the layers
            layer = mshr.Rectangle(Point(left, 0.), Point(right, 1.)) #creating a layer with the geometric info
            domain.set_subdomain(i + 1, layer) #marks inclusions with domain larger than zero
        
    mesh = mshr.generate_mesh(domain, resolution) #generates the mesh with the desired resolution
    
    subdomains = MeshFunction('size_t', mesh, 2, mesh.domains()) #creates the subdomains
    # Mark subdomain as 1
    for i in range(subdomains.size()): #marks all the inclusions with subdomain = 1
        if subdomains[i] > 0:
            subdomains[i] = 1
    return mesh,subdomains

def refine_mesh(times,mesh,subdomains):
    '''
    refines the mesh n times with mshr libray
        Args:
        times: how many times to refine
        mesh: mesh 
        subdomains:subdomains
    Returns:
        the refined mesh and geometries
    '''
    for t in range(times):
        need_refine = MeshFunction("bool", mesh, 2, False)
        for c in cells(mesh):
            if subdomains[c] > 0:
                need_refine[c] = True
        mesh = refine(mesh, need_refine)
        subdomains = adapt(subdomains, mesh)
    return mesh,subdomains
