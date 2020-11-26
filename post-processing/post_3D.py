import sys
sys.path.insert(1,"../numerical_analysis")
sys.path.insert(2,"../analytical")
import numpy as np
from dolfin import *
import matplotlib as plt
from epilysis_3D import calculate_Volume_fraction 
from epilysis3D_functions import applied_strain, stress, stress_Voigt_generic
import analytical
import scipy.linalg as sc
from datetime import datetime
import store

def print_moduli (name,E_xx=None,E_yy=None,E_zz=None,Gxy=None,Gyz=None,Gzx=None,results_location="./results"):
    """
    Prints the elastic moduli tensor 
    Args:
        name
        C: effective elastic moduli tensor
        E_xx,E_yy,E_zz,Gxy,Gxy,Gzx: solution to be compared to
    Prints:
        Elastic moduli tensor 
        Bxx,Byy,Bzz: Bulk Modulus
        Exx,Eyy,Ezz: Young Modulus
        Gxy,Gyz,Gzx: Shear Modulus
        Error if given analytical results
    """
    C = np.genfromtxt(results_location+"/3D/"+ name + "_C.txt", dtype=float)
    print("C \n", C)
    C_inv = sc.inv(C)
    print("Calculated Bxx from C: ",(C[0,0] + 2 * C[0,1])/3)
    print("Calculated Byy from C: ",(C[1,1] + 2 * C[1,2])/3)
    print("Calculated Bzz from C: ",(C[2,2] + 2 * C[2,1])/3)
    print("Calculated Exx from C.inverse : ", 1/C_inv[0,0])
    print("Divergence Exx = ", (1/C_inv[0,0] - E_xx)/E_xx) if E_xx != None else ""
    print("Calculated Eyy from C.inverse: ", 1/C_inv[1,1])
    print("Divergence Eyy = ", (1/C_inv[1,1] - E_yy)/E_yy) if E_yy != None else ""
    print("Calculated Ezz from C.inverse: ", 1/C_inv[2,2])
    print("Divergence Eyy = ", (1/C_inv[2,2] - E_zz)/E_zz) if E_zz != None else ""
    print("Calculated Gyz from C.inverse", 1/C_inv[3,3])
    print("Calculated Gyz from C: ", C[3,3])
    print("Divergence Gyz = ", (1/C_inv[3,3] - Gyz)/Gyz) if Gyz != None else ""
    print("Calculated Gxz from C.inverse", 1/C_inv[4,4])
    print("Calculated Gxz from C: ", C[4,4])
    print("Divergence Gzx = ", (1/C_inv[4,4] - Gzx)/Gzx) if Gzx != None else ""
    print("Calculated Gxy from C.inverse", 1/C_inv[5,5])
    print("Calculated Gxy from C: ", C[5,5])
    print("Divergence Gxy = ", (1/C_inv[5,5] - Gxy)/Gxy) if Gxy != None else ""
    return 

def layers_comparison(name,mesh,subdomains,E=None,nu=None,results_location="./results"):
    """
    Benchmarks solution against Voigt-Reuss averages 
    Args:
        name
        C: effective elastic moduli tensor
        E,nu: phases Young modulus and Poisson's ratio
    Prints:
        Error compared to Voigt-Reuss averages
    """
    if type(E) != np.array:
        E = np.genfromtxt(results_location+"/3D/Data/"+ name + "_E.txt", dtype=float)
        nu = np.genfromtxt(results_location+"/3D/Data/"+ name + "_nu.txt", dtype=float)
    G = E / 2 / (1+nu)
    v_1 = calculate_Volume_fraction(mesh,subdomains)
    v_0 = 1. - v_1
    E_yy,E_xx = analytical.Voigt_Reuss(v_0,v_1,E[0],E[1])
    E_zz = E_yy
    print("Exx = ", E_xx)
    print("Eyy = ", E_yy)
    print("Ezz = ", E_zz)
    G_yz,G_xy = analytical.Voigt_Reuss(v_0,v_1,G[0],G[1])
    G_zx = G_xy
    print("Gyz = ", G_yz)
    print("Gxy = ", G_xy)
    print("Gxz = ", G_zx)
    print_moduli(name,E_xx,E_yy,E_zz,G_xy,G_yz,G_zx,results_location=results_location)
    return E_xx,E_yy,E_zz,G_xy,G_yz,G_zx

def spheroid_comparison(name,mesh,subdomains,vol_frac=None,aspect_ratio=1,E=None,nu=None,C=None,results_location="./results"):
    if type(E) != np.array:
        #Make sure you have saved E,nu after defining the material (store.save_E_nu_iso(name,E,nu))
        E = np.genfromtxt(results_location+"/3D/Data/"+ name + "_E.txt", dtype=float)
        nu = np.genfromtxt(results_location+"/3D/Data/"+ name + "_nu.txt", dtype=float)
        C = np.genfromtxt(results_location+"/3D/"+ name + "_C.txt", dtype=float)
    if  vol_frac == None:
        vol_frac = calculate_Volume_fraction(mesh,subdomains)
        print(vol_frac)
    C_an = analytical.Mori_Tanaka_fm(E,nu,aspect_ratio,vol_frac)
    return abs(np.sum(C_an) - np.sum(C)) / abs(np.sum(C_an)) *100

def Voigt_Reuss_comparison(name,mesh,subdomains,v_1=None,E=None,nu=None,C=None,results_location="./results"):
    if type(E) != np.array:
        E = np.genfromtxt(results_location+"/3D/Data/"+ name + "_E.txt", dtype=float)
        nu = np.genfromtxt(results_location+"/3D/Data/"+ name + "_nu.txt", dtype=float)
        C = np.genfromtxt(results_location+"/3D/"+ name + "_C.txt", dtype=float)
    C_inv = sc.inv(C)
    Exx_num = 1/C_inv[0,0]
    Eyy_num = 1/C_inv[1,1]
    Ezz_num = 1/C_inv[2,2]
    Gyz_num = C[3,3]
    Gzx_num = C[4,4]
    Gxy_num = C[5,5]
    G = E / 2 / (1+nu)
    if  v_1 == None:
        v_1 = calculate_Volume_fraction(mesh,subdomains)
    v_0 = 1. - v_1
    E_yy,E_xx = analytical.Voigt_Reuss(v_0,v_1,E[0],E[1])
    E_zz = E_yy
    G_yz,G_xy = analytical.Voigt_Reuss(v_0,v_1,G[0],G[1])
    G_zx = G_xy
    error_xx = abs(Exx_num - E_xx) / (E_xx)
    error_yy = abs(Eyy_num - E_yy) / (E_yy)
    error_zz = abs(Ezz_num - E_zz) / (E_zz)
    error_yz = abs(Gyz_num - G_yz) / (G_yz)
    error_zx = abs(Gzx_num - G_zx) / (G_zx)
    error_xy = abs(Gxy_num - G_xy) / (G_xy)
#    print(Exx_num,E_xx)
#    print(Eyy_num,E_yy)
#    print(Ezz_num,E_zz)
#    print(Gyz_num,G_yz)
#    print(Gzx_num,G_zx)
#    print(Gxy_num,G_xy) 
    return (error_xx+error_yy+error_zz+error_yz+error_zx+error_xy) / 6 *100

def bounds(name,mesh,subdomains,E=None,nu=None,C=None,aspect_ratio=1,results_location="./results"):
    """
    Gives the Reuss/Voigt bounds and the Mori Tanaka solution for K and G  
    Args:
        name
        C: effective elastic moduli tensor
        E,nu: phases Young modulus and Poisson's ratio
        aspect_ratio: aspect ratio for Proalte Spheroids > 1
    Return:
        bounds
    """
    if type(E) != np.array:
        #Make sure you have saved E,nu after defining the material (store.save_E_nu_iso(name,E,nu))
        E = np.genfromtxt(results_location+"/3D/Data/"+ name + "_E.txt", dtype=float)
        nu = np.genfromtxt(results_location+"/3D/Data/"+ name + "_nu.txt", dtype=float)
        C = np.genfromtxt(results_location+"/3D/"+ name + "_C.txt", dtype=float)
    G = E / 2 / (1+nu)
    K = E / 3 / (1-2*nu)
    s = E[0] / E[1]
    vol_frac = calculate_Volume_fraction(mesh,subdomains)
    K_Voigt,K_Reuss = analytical.Voigt_Reuss(1-vol_frac,vol_frac,K[0],K[1]) #Reuss-Voigt Bounds
    G_Voigt,G_Reuss = analytical.Voigt_Reuss(1-vol_frac,vol_frac,G[0],G[1])
    C_Mori_Tanaka = analytical.Mori_Tanaka_fm(E,nu,aspect_ratio,vol_frac)
    K_Mori_Tanaka = (C_Mori_Tanaka[0,0] + 2 * C_Mori_Tanaka[0,1])/3
    G_Mori_Tanaka = (C_Mori_Tanaka[3,3])
    K_num = ((C[0,0] + 2 * C[0,1])/3+(C[1,1] + 2 * C[1,2])/3+(C[2,2] + 2 * C[2,1])/3) / 3
    G_num = (C[3,3]+C[4,4]+C[5,5])/3
    store.save_graphs(name,vol_frac,s,C,K_Voigt,K_Reuss,G_Voigt,G_Reuss,K_Mori_Tanaka,G_Mori_Tanaka,K_num,G_num,results_location=results_location)
    return K_Voigt,K_Reuss,K_Mori_Tanaka,K_num,G_Voigt,G_Reuss,G_Mori_Tanaka,G_num

def b_f(vol_frac,E,nu,aspect_ratio=1):
    """
    Gives the Reuss/Voigt bounds and the Mori Tanaka solution for K and G with given the desired volume fraction
    Args:
        name
        C: effective elastic moduli tensor
        E,nu: phases Young modulus and Poisson's ratio
        aspect_ratio: aspect ratio for Proalte Spheroids > 1
        vol_frac: desired volume fraction
    Return:
        Bounds
    """    
    G = E / 2 / (1+nu)
    K = E / 3 / (1-2*nu)
    K_Voigt,K_Reuss = analytical.Voigt_Reuss(1-vol_frac,vol_frac,K[0],K[1]) #Reuss-Voigt Bounds
    G_Voigt,G_Reuss = analytical.Voigt_Reuss(1-vol_frac,vol_frac,G[0],G[1])
    C_Mori_Tanaka = analytical.Mori_Tanaka_fm(E,nu,aspect_ratio,vol_frac)
    K_Mori_Tanaka = ((C_Mori_Tanaka[0,0] + 2 * C_Mori_Tanaka[0,1])/3+(C_Mori_Tanaka[1,1] + 2 * C_Mori_Tanaka[1,2])/3+(C_Mori_Tanaka[2,2] + 2 * C_Mori_Tanaka[2,1])/3) / 3
    G_Mori_Tanaka = C_Mori_Tanaka[3,3]
    return K_Voigt,K_Reuss,K_Mori_Tanaka,G_Voigt,G_Reuss,G_Mori_Tanaka
    