import sys
sys.path.insert(1,"../numerical_analysis")
sys.path.insert(2,"../analytical")
import numpy as np
from dolfin import *
import matplotlib as plt
from epilysis_functions import applied_strain, stress_Voigt_generic, stress
from epilysis import calculate_Volume_fraction 
from analytical import Voigt_Reuss
import i_o

def print_moduli (name,C=None,E_xx=None,E_yy=None,G=None,results_location=",./results"):
    """
    Prints the elastic moduli tensor 
    Args:
        name
        C: effective elastic moduli tensor
        E_xx,E_yy,G: solution to be compared to
    Prints:
        Elastic moduli tensor 
        Exx,Eyy,G
        Error if given analytical results
    """
    if type(C) != np.array:
        C = i_o.read_C(name,results_location)        
    print("C \n", C)
    C_inv = np.linalg.inv(C)
    print("Calculated Exx from C.inverse : ", 1/C_inv[0,0])
    print("Divergence Exx = ", ((1/C_inv[0,0]) - E_xx)/E_xx) if E_xx != None else ""
    print("Calculated Eyy from C.inverse: ", 1/C_inv[1,1])
    print("Divergence Eyy = ", ((1/C_inv[1,1]) - E_yy)/E_yy) if E_yy != None else ""
    print("Calculated G from C.inverse: ", 1/C_inv[2,2])
    print("Divergence G = ", ((1/C_inv[2,2]) - G)/G) if G != None else ""
    return 0 

def layers_comparison(name,C=None,E=None,nu=None,mesh=None,subdomains=None,results_location="./results"):
    """
    Benchmarks solution against Voigt-Reuss averages 
    Args:
        name
        C: effective elastic moduli tensor
        E,nu: phases Young modulus and Poisson's ratio
    Prints:
        Error compared to Voigt-Reuss averages
    """
    if type(C) != np.array:
        C=i_o.read_C(name,results_location)
        E,nu = i_o.read_E_nu(name,results_location)
    G = E / 2 / (1+nu)
    v_1 = calculate_Volume_fraction(mesh,subdomains)
    v_0 = 1. - v_1
    E_yy,E_xx = Voigt_Reuss(v_0,v_1,E[0],E[1])
    print("Exx = ", E_xx)
    print("Eyy = ", E_yy)
    G_xy,G_yx = Voigt_Reuss(v_0,v_1,G[0],G[1])
    print("Gxy = ", G_xy)
    print("Gyx = ", G_yx)
    print_moduli(name,C,E_xx,E_yy,G_yx,results_location)
    return E_xx,E_yy,G_xy,G_yx