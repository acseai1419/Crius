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

#3D
#------------------------------------------------------------------------
#------------------------------------------------------------------------
meshes_location = "../meshes"
paraview_location = "../paraview"
results_location = "../results"
#------------------------------------------------------------------------
#------------------------------------------------------------------------
name = "Spherical_Inclusions_10"
#store.save_name(name,results_location) #save the name for the post-processing!!!
#-------------------------------------------------------------------------
#-------------------------------------------------------------------------
mesh = Mesh(meshes_location+"/gmsh/" + name + ".xml")
subdomains = MeshFunction("size_t", mesh, meshes_location+"/gmsh/" + name + "_physical_region.xml")
store.save_mesh(name,mesh,subdomains,meshes_location,paraview_location)
a=1
b=1
c=1
vertices = np.array([[0, 0.,0.],#0
                     [a, 0.,0.],#1
                     [a,0.,c],#2
                     [0.,0.,c],#3
                     [0.,b,c],#4
                     [0.,b,0.],#5
                     [a,b,0.],#6
                     [a,b,c]])#7
vol = a*b*c

C_phases = np.zeros((2,6,6))
C_1 = np.diag([1,1,1,1,1,1])
C_2 = np.diag([1,1,1,1,1,1])
C_phases[0::] = C_1
C_phases[1::] = C_2
#Exx,Eyy,Ezz,Gxy,Gzx,Gyz,nuxy,nuzx,nuyz = ep3f.ortho_from_iso(E,nu)
#store.save_E_nu_iso(name,E,nu,results_location) #save E,nu for the post-processing!!!
#-------------------------------------------------------------------------
dx,w,Eps,F,a,L = epilysis_3D.fe_problem(mesh,subdomains,vertices,C_gen=C_phases)
C_guess = epilysis_3D.calculate_moduli(name,mesh,vol,dx,w,Eps,F,a,L,C_gen=C_phases,mesh_location=meshes_location,paraview_location=paraview_location,results_location=results_location)
#-------------------------------------------------------------------------
print(np.round(C_guess,3))