import sys
sys.path.insert(3,"../pre-processing/3D")
sys.path.insert(1,"../numerical_analysis")
sys.path.insert(2,"../analytical")
sys.path.insert(5,"../post-processing")
import numpy as np
from dolfin import *
import matplotlib.pyplot as plt
import scipy.linalg as sc
import epilysis3D_functions as ep3f
import epilysis_3D
import store
import post_3D

#3D
#------------------------------------------------------------------------
#------------------------------------------------------------------------
meshes_location = "../meshes"
paraview_location = "../paraview"
results_location = "../results"
#------------------------------------------------------------------------
#------------------------------------------------------------------------
def error_char_length(E,nu,vol_frac,error,j):
    for i,name in enumerate([str('{:0.2f}'.format(vol_frac))[2:]+"_l_length_70",str('{:0.2f}'.format(vol_frac))[2:]+"_l_length_60",str('{:0.2f}'.format(vol_frac))[2:]+"_l_length_50",str('{:0.2f}'.format(vol_frac))[2:]+"_l_length_40",str('{:0.2f}'.format(vol_frac))[2:]+"_l_length_25",str('{:0.2f}'.format(vol_frac))[2:]+"_l_length_20",str('{:0.2f}'.format(vol_frac))[2:]+"_l_length_15",str('{:0.2f}'.format(vol_frac))[2:]+"_l_length_10",str('{:0.2f}'.format(vol_frac))[2:]+"_l_length_05"]):
        store.save_name(name,results_location=results_location) #save the name for the post-processing!!!
        #-------------------------------------------------------------------------
        #-------------------------------------------------------------------------
        mesh = Mesh(meshes_location+"/gmsh/" + name + ".xml")
        subdomains = MeshFunction("size_t", mesh, meshes_location+"/gmsh/" + name + "_physical_region.xml")
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
        Exx,Eyy,Ezz,Gxy,Gzx,Gyz,nuxy,nuzx,nuyz = ep3f.ortho_from_iso(E,nu)
        store.save_E_nu_iso(name,E,nu,results_location=results_location) #save E,nu for the post-processing!!!
        #-------------------------------------------------------------------------
        dx,w,Eps,F,a,L = epilysis_3D.fe_problem(mesh,subdomains,vertices,Exx,Eyy,Ezz,Gxy,Gzx,Gyz,nuxy,nuzx,nuyz)
        epilysis_3D.calculate_moduli(name,mesh,vol,dx,w,Eps,F,a,L,Exx,Eyy,Ezz,Gxy,Gzx,Gyz,nuxy,nuzx,nuyz,mesh_location = meshes_location, paraview_location = paraview_location, results_location = results_location)
        #-------------------------------------------------------------------------
        error[j,i] = (post_3D.Voigt_Reuss_comparison(name,mesh,subdomains,vol_frac,results_location=results_location))
    return error
        
E = np.array([1000.,500.],dtype = np.longlong)
nu = np.array([0.2,0.2],dtype = np.longlong)
volume_fraction = [0.25,0.50,0.75]
lengths = np.array([70,60,50,40,25,20,15,10,5]) / 100
error = np.zeros((len(volume_fraction),len(lengths)))
for j,vol_frac in enumerate(volume_fraction):
    error = error_char_length(E,nu,vol_frac,error,j)

fig, ax1 = plt.subplots(1, 1, figsize=(8, 5))
for j in range(len(volume_fraction)):
    ax1.plot(lengths,error[j,:], '--', label='Error for volume fraction = {}'.format(volume_fraction[j]))
    ax1.set_xlabel('$Characteristic\ Length$', fontsize=14)
    ax1.set_ylabel('$Error\ (\%)$', fontsize=14)
    ax1.set_title('Volume Fraction = {}'.format(volume_fraction), fontsize=16)
    ax1.legend(loc='best', fontsize=14)
'{:0.2f}'.format(vol_frac)