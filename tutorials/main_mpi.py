import time
import sys
sys.path.insert(3,"../pre-processing/3D")
sys.path.insert(4,"../pre-processing")
sys.path.insert(1,"../numerical_analysis")
sys.path.insert(2,"../analytical")
sys.path.insert(5,"../post-processing")
import numpy as np
from dolfin import *
import matplotlib as plt
import scipy.linalg as sc
import epilysis3D_functions as ep3f
import epilysis_3D
import post_3D
#3D
#------------------------------------------------------------------------
#------------------------------------------------------------------------
meshes_location = "../meshes"
paraview_location = "../paraview"
results_location = "../results"
#------------------------------------------------------------------------
#------------------------------------------------------------------------
name = "bulit_in"
#------------------------------------------------------------------------
mesh = Mesh()
hdf = HDF5File(mesh.mpi_comm(), meshes_location+"/mpi_mesh/file.h5", "r")
hdf.read(mesh, "/mesh", False)
subdomains = MeshFunction("size_t", mesh,mesh.topology().dim())
hdf.read(subdomains, "/subdomains")

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

E = np.array([100,100],dtype = np.longlong)
nu = np.array([0.2,0.2],dtype = np.longlong)
Exx,Eyy,Ezz,Gxy,Gzx,Gyz,nuxy,nuzx,nuyz = ep3f.ortho_from_iso(E,nu)
#-------------------------------------------------------------------------
start = time.time()
dx,w,Eps,F,a,L = epilysis_3D.fe_problem(mesh,subdomains,vertices,Exx,Eyy,Ezz,Gxy,Gzx,Gyz,nuxy,nuzx,nuyz)
C_guess = epilysis_3D.calculate_moduli(name,mesh,vol,dx,w,Eps,F,a,L,Exx,Eyy,Ezz,Gxy,Gzx,Gyz,nuxy,nuzx,nuyz,meshes_location,paraview_location,results_location)
end = time.time()
#-------------------------------------------------------------------------
print(end-start)
print(np.round(C_guess,3))
