import sys
sys.path.insert(3,"../pre-processing/3D")
sys.path.insert(1,"../numerical_analysis")
sys.path.insert(2,"../analytical")
sys.path.insert(5,"../post-processing")
import numpy as np
from dolfin import *
import matplotlib as plt
import scipy.linalg as sc
import epilysis3D_functions as ep3f
import epilysis_3D
import store

set_log_level(10)
#3D
#------------------------------------------------------------------------
#------------------------------------------------------------------------
meshes_location = "../meshes"
paraview_location = "../paraview"
results_location = "../results"
#------------------------------------------------------------------------
#------------------------------------------------------------------------
name = "Spherical_Inclusions_30"
#name = "pygalmesh_1m"
#name = "bulit_in"
#name = "built_in_new"

store.save_name(name,results_location) #save the name for the post-processing!!!
#-------------------------------------------------------------------------
#-------------------------------------------------------------------------
mesh = Mesh(meshes_location+"/gmsh/" + name + ".xml")
subdomains = MeshFunction("size_t", mesh, meshes_location+"/gmsh/" + name + "_physical_region.xml")
store.save_mesh(name,mesh,subdomains,meshes_location,paraview_location)
#----------------------------------------------------------------------------------
xmin = mesh.coordinates()[:, 0].min()
ymin = mesh.coordinates()[:, 1].min()
zmin = mesh.coordinates()[:, 2].min()

xmax= mesh.coordinates()[:, 0].max()
ymax = mesh.coordinates()[:, 1].max()
zmax = mesh.coordinates()[:, 2].max()
a= xmax - xmin
b= ymax - ymin
c= zmax - zmin
vertices = np.array([[xmin,ymin,zmin],#0
                     [xmax, ymin,zmin],#1
                     [xmax,ymin,zmax],#2
                     [xmin,ymin,zmax],#3
                     [xmin,ymax,zmax],#4
                     [xmin,ymax,zmin],#5
                     [xmax,ymax,zmin],#6
                     [xmax,ymax,zmax]])#7
vol = a*b*c
print(vertices)

#a=1
#b=1
#c=1
#vertices = np.array([[0, 0.,0.],#0
#                     [a, 0.,0.],#1
#                     [a,0.,c],#2
#                     [0.,0.,c],#3
#                     [0.,b,c],#4
#                     [0.,b,0.],#5
#                     [a,b,0.],#6
#                     [a,b,c]])#7
#
#vol = a*b*c
#print(vertices)
#------------------------------------------------------------------------------------
E = np.array([100,100.],dtype = np.longlong)
nu = np.array([0.2,0.2],dtype = np.longlong)

Exx,Eyy,Ezz,Gxy,Gzx,Gyz,nuxy,nuzx,nuyz = ep3f.ortho_from_iso(E,nu)
store.save_E_nu_iso(name,E,nu,results_location) #save E,nu for the post-processing!!!
#-------------------------------------------------------------------------
dx,w,Eps,F,a,L = epilysis_3D.fe_problem(mesh,subdomains,vertices,Exx,Eyy,Ezz,Gxy,Gzx,Gyz,nuxy,nuzx,nuyz)
print("Solving the equation ...")
C_guess = epilysis_3D.calculate_moduli(name,mesh,vol,dx,w,Eps,F,a,L,Exx,Eyy,Ezz,Gxy,Gzx,Gyz,nuxy,nuzx,nuyz,meshes_location,paraview_location,results_location)
#-------------------------------------------------------------------------
print(np.round(C_guess,3))