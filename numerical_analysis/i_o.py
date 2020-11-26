from dolfin import *
import numpy as np

def save_mesh(name,mesh,subdomains,meshes_location = "./meshes",paraview_location = "./paraview"):
    File(meshes_location +"/2D/" + name + ".xml") << mesh
    File(meshes_location +"/2D/" + name + "_physical_region.xml") << subdomains
    File(paraview_location +"/2D/" + name + "_physical_region.pvd") << subdomains
    return 0

def save_name(name,results_location="./results"):
    text_file = open(results_location+"/2D/Data/name.txt", "w")
    text_file.write(name)
    text_file.close()
    
def save_elast_moduli(C,C0,C1,name,results_location="./results"):
    np.savetxt(results_location+"/2D/" + name + "_C.txt", C)
    np.savetxt(results_location+"/2D/" + name + "_C_0.txt", C0)
    np.savetxt(results_location+"/2D/" + name + "_C_1.txt", C1)
    
def save_E_nu(name,Exx=None,Eyy=None,nuxy=None,Gxy=None,results_location = "./results"):
    np.savetxt(results_location+"/2D/Data/" + name + "_Exx.txt", Exx) 
    np.savetxt(results_location+"/2D/Data/" + name + "_Eyy.txt", Eyy)
    np.savetxt(results_location+"/2D/Data/" + name + "_nuxy.txt", nuxy)
    np.savetxt(results_location+"/2D/Data/" + name + "_Gxy.txt", Gxy)

def save_E_nu_iso(name,Exx=None,nuxy=None,results_location = "./results"):
    np.savetxt(results_location+"/2D/Data/" + name + "_Exx.txt", Exx) 
    np.savetxt(results_location+"/2D/Data/" + name + "_nuxy.txt", nuxy)

def read_name(results_location = "./results"):
    return open(results_location+'/2D/Data/name.txt', 'r').read()
    
def read_C(name, results_location = "./results"):
    return np.genfromtxt(results_location+"/2D/"+ name + "_C.txt", dtype=float)

def read_E_nu(name,results_location = "./results"):
    E = np.genfromtxt(results_location+"/2D/Data/"+ name + "_Exx.txt", dtype=float)
    nu = np.genfromtxt(results_location+"/2D/Data/"+ name + "_nuxy.txt", dtype=float)
    return E,nu