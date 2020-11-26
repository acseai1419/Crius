import sys
sys.path.insert(1,"../numerical_analysis")
sys.path.insert(2,"../analytical")
sys.path.insert(3,"../pre-processing/2D")
sys.path.insert(4,"../post-processing")
import numpy as np
from dolfin import *
import matplotlib as plt
import scipy.linalg as sc
from datetime import datetime
import create_circular_incl as circ_incl
import create_layers
import create_mesh as gen_mesh
import epilysis_functions as epf
import epilysis
import i_o
import post
#2D
#------------------------------------------------------------------------
#------------------------------------------------------------------------
meshes_location = "../meshes"
paraview_location = "../paraview"
results_location = "../results"
#------------------------------------------------------------------------
#------------------------------------------------------------------------
###Generate material with circular inclusions
##case(1)
#name = "circular_inclusions_015"
#resolution = 100
##porosity, min_rad, max_rad
#rad = circ_incl.get_parameters(0.40,0.1,0.15)
#inclusions = circ_incl.create_dataset(name,len(rad),rad,meshes_location=meshes_location,inside=True)
##-----------------------------------------------------------------------
##------------------------------------------------------------------------
##case(2)number of circles, radius, 10 circles of radius 0.1
name = "circular_inclusions_n"
resolution = 100
rad = np.full(10,.1)
inclusions = circ_incl.create_dataset(name,len(rad),rad,meshes_location=meshes_location)
##------------------------------------------------------------------------
##------------------------------------------------------------------------
#case(3) Generate laminated composite
#name = "layers"
#resolution = 100
#x = [0.1,0.3,0.5,0.7,0.9]
#inclusions = create_layers.create_dataset(meshes_location = meshes_location)
#------------------------------------------------------------------------
#Numerical Analysis
#------------------------------------------------------------------------
mesh,subdomains = gen_mesh.create_mesh_2D(name,resolution,inclusions,meshes_location = meshes_location)
#mesh,subdomains = gen_mesh.refine_mesh(1,mesh,subdomains)
i_o.save_mesh(name,mesh,subdomains,meshes_location,paraview_location)
#i_o.save_name(name,results_location)
##-------------------------------------------------------------------------
##-------------------------------------------------------------------------
a=1
b=1
vertices = np.array([[0, 0.],
                     [a, 0.],
                     [a, b],
                     [0, b]])
area = a*b
E = np.array([100,50],dtype = np.longlong)
nu = np.array([0.2,0.3],dtype = np.longlong)

Exx,Eyy,nuxy,Gxy = epf.ortho_from_iso(E,nu)
##-------------------------------------------------------------------------
dx,w,Eps,F,a,L = epilysis.fe_problem(mesh,subdomains,vertices,area,Exx,Eyy,nuxy,Gxy)
C_guess = epilysis.calculate_moduli(name,mesh,area,dx,w,Eps,F,a,L,Exx,Eyy,nuxy,Gxy,meshes_location=meshes_location,results_location=results_location,paraview_location=paraview_location)
#-------------------------------------------------------------------------
#-------------------------------------------------------------------------
#-------------------------------------------------------------------------
#case -4 Gmsh (we use this when we want to solve domain with crossing boundaries)
#name = "periodic_circular_inclusions"
#mesh = Mesh(meshes_location+"/gmsh/" + name + ".xml")
#subdomains = MeshFunction("size_t", mesh, meshes_location+"/gmsh/" + name + "_physical_region.xml")
#a=1
#b=1
#vertices = np.array([[0, 0.],
#                     [a, 0.],
#                     [a, b],
#                     [0, b]])
#area = a*b
#E = np.array([100,50],dtype = np.longlong)
#nu = np.array([0.2,0.3],dtype = np.longlong)
#
#Exx,Eyy,nuxy,Gxy = epf.ortho_from_iso(E,nu)
#dx,w,Eps,F,a,L = epilysis.fe_problem(mesh,subdomains,vertices,area,Exx,Eyy,nuxy,Gxy)
#C_guess = epilysis.calculate_moduli(name,mesh,area,dx,w,Eps,F,a,L,Exx,Eyy,nuxy,Gxy,meshes_location=meshes_location,results_location=results_location,paraview_location=paraview_location)
##--------------------------------------------------------------------------
##Post-processing
##--------------------------------------------------------------------------
if name == "layers":
    post.layers_comparison(name,C_guess,E,nu,mesh,subdomains,results_location=results_location)
else:
    post.print_moduli(name,C_guess,results_location=results_location)
