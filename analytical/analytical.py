import numpy as np
import fiberpy.mechanics as fm

def Voigt_Reuss(f1,f2,M1,M2):
    """
    Calculates the Voigt and Reuss averages
    Args:
        name
        f1,f2: volume fractions of each phase
        M1,M2: Modulus of each phase
    Return:
        Voigt and Reuss averages
    """
    Voigt_average = f1*M1 + f2*M2
    Reuss_average = f1/M1 + f2/M2
    return Voigt_average, 1/Reuss_average 

def Mori_Tanaka(E,nu,axes_ratio,vol_frac):
    """
    Calculates the Mori Tanaka solution
    Args:
        E,nu: Young moduli and Poisson ratios
        axes_ratio: aspect ratio
        vol_frac
    Return
        Elastic moduli tensor 
    Code from:
        https://gist.github.com/harjinder784/67b36ba197b2ad4e43d62fab2526da2a
    """
    if axes_ratio==1:
        axes_ratio+=0.01
    #Eshelby Inclusions - Eshelby Matrix
    Q = 3 / 8 / (1 - nu[0])
    R = (1 - 2*nu[0]) / 8 / (1-nu[0])
    I1 = (2 * axes_ratio / (axes_ratio**2 - 1)**1.5) * (axes_ratio * (axes_ratio**2 - 1)**0.5 - np.arccosh(axes_ratio))
    T = Q * (4 - 3 * I1) / (3*(axes_ratio**2 - 1))
    I3 = 4 - 2*I1
    
    S = np.zeros((6,6))
    S[0,0] = Q + R*I1 + 0.75 * T
    S[1,1] = S[0,0]
    S[2,2] = 4./3 * Q + R*I3 + 2*axes_ratio**2 * T
    S[0,1] = Q / 3 - R*I1 + 4 * T/3
    S[1,0] = S[0,1]
    S[0,2] = -R * I1 - axes_ratio**2*T
    S[1,2] = S[0,2]
    S[2,0] = -R*I3 - T
    S[2,1] = S[2,0]
    S[5,5] = Q/3 + R*I1 + T/4
    S[3,3] = 2 * R - I1 * R / 2 - (1 + axes_ratio**2) * T / 2
    S[4,4] = S[3,3]
    
    C_incl = np.zeros((6,6))
    C_incl[0:3,0:3] = nu[1]*np.ones((3,3))
    C_incl = C_incl + (1.-2.*nu[1])*np.eye(6)
    C_incl[3:,3:] = C_incl[3:,3:]/2.
    C_incl = E[1]/((1.+nu[1])*(1.-2.*nu[1]))*C_incl
    
    C_matrix = np.zeros((6,6))
    C_matrix[0:3,0:3] = nu[0]*np.ones((3,3))
    C_matrix = C_matrix + (1.-2.*nu[0])*np.eye(6)
    C_matrix[3:,3:] = C_matrix[3:,3:]/2.
    C_matrix = E[0]/((1+nu[0])*(1.-2.*nu[0]))*C_matrix
    
    A_e = np.linalg.inv(np.eye(6)+np.dot(np.dot(S,np.linalg.inv(C_matrix)),C_incl-C_matrix))
    A_mt = np.dot(A_e,np.linalg.inv(vol_frac*A_e+(1-vol_frac)*np.eye(6)))
    
    C_uni = C_matrix + vol_frac*np.dot(C_incl-C_matrix,A_mt)
    return C_uni

    
def Mori_Tanaka_fm(E,nu,aspect_ratio,vol_frac):
    """
    Calculates the Mori Tanaka solution
    Args:
        E,nu: Young moduli and Poisson ratios
        axes_ratio: aspect ratio for spheroids
        vol_frac: volume fraction for second phase
    Return
        Elastic moduli tensor 
    Reference:
       https://github.com/tianyikillua/fiberpy
    """
    if aspect_ratio==1:
        aspect_ratio+=0.001
    rve_data = {
    "rho0": 1,
    "E0": E[0],
    "nu0": nu[0],
    "alpha0": 1,
    "rho1": 1,
    "E1": E[1],
    "nu1": nu[1],
    "alpha1": 1,
    "mf": vol_frac,
    "aspect_ratio": aspect_ratio,
    }
    mat = fm.FiberComposite(rve_data)
    return (mat.ABar(np.array([0,0,0]),"MoriTanaka",closure="orthotropic"))

def TandonWeng_fm(E,nu,aspect_ratio,vol_frac):
    """
    Calculates the Tendon Wang solution
    Args:
        E,nu: Young moduli and Poisson ratios
        axes_ratio: aspect ratio for spheroids
        vol_frac : volume fraction of second phase
    Return
        Elastic moduli tensor 
    Reference:
       https://github.com/tianyikillua/fiberpy
    """
    if aspect_ratio==1:
        aspect_ratio+=0.001
    rve_data = {
    "rho0": 1,
    "E0": E[0],
    "nu0": nu[0],
    "alpha0": 1,
    "rho1": 1,
    "E1": E[1],
    "nu1": nu[1],
    "alpha1": 1,
    "mf": vol_frac,
    "aspect_ratio": aspect_ratio,
    }
    mat = fm.FiberComposite(rve_data)
    return (mat.ABar(np.array([0,0,0]),"TandonWeng",closure="orthotropic"))