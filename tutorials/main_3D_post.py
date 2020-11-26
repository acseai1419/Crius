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
import post_3D

results_location="../results"
paraview_location="../paraview"
mesh_location="../meshes"

name = open(results_location+'/3D/Data/name.txt', 'r').read()#If the name is read from results make sure it was saved when defining the problem
mesh = Mesh(mesh_location+"/gmsh/" + name + ".xml")
subdomains = MeshFunction("size_t", mesh, mesh_location+"/gmsh/"+ name + "_physical_region.xml")
#In the next two functions E,nu is read from the results, they are saved when defining the problem (store.save_E_nu_iso(name,E,nu))
post_3D.print_moduli(name,results_location=results_location)
print(post_3D.spheroid_comparison(name,mesh,subdomains,results_location=results_location))
print(post_3D.bounds(name,mesh,subdomains,aspect_ratio = 4,results_location=results_location))
#---------------------------------------------------------------------------------------------------
#post_3D.layers_comparison(name,mesh,subdomains,results_location=results_location)