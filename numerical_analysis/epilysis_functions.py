from dolfin import *
import numpy as np

class PeriodicBoundary(SubDomain):
    """
    Periodic Boundaries to be imported in the numerical analysis
    Args:
        vertices: vertices of the rectangle
        tolerance: tolerance for periodicity
        x: set of coordinates x(x,y) in 2D
        y: set of coordinates for periodic extension y(x,y)
    Defines:
        Full periodic boundaries for the numerical analysis
    Reference:
        Bleyer, J., 2018. Numerical tours of continuum mechanics using FEniCS
    """
    def __init__(self, vertices, tolerance=DOLFIN_EPS):
        SubDomain.__init__(self, tolerance)
        self.tol = tolerance
        self.vv = vertices
        self.a1 = self.vv[1,:]-self.vv[0,:] #distance in x direction 
        self.a2 = self.vv[3,:]-self.vv[0,:] #distance in y direction
        
    def inside(self, x, on_boundary):
        """
        Returns True when on left or bottom and False on bottom-right or top-left
        """
        return bool((near(x[0], self.vv[0,0] + x[1]*self.a2[0]/self.vv[3,1], self.tol) or 
                     near(x[1], self.vv[0,1] + x[0]*self.a1[1]/self.vv[1,0], self.tol)) and 
                     (not ((near(x[0], self.vv[1,0], self.tol) and near(x[1], self.vv[1,1], self.tol)) or 
                     (near(x[0], self.vv[3,0], self.tol) and near(x[1], self.vv[3,1], self.tol)))) and on_boundary)

    def map(self, x, y):
        """
        Maps the boundaries
        """
        if near(x[0], self.vv[2,0], self.tol) and near(x[1], self.vv[2,1], self.tol): # top-right corner
            y[0] = x[0] - (self.a1[0]+self.a2[0])
            y[1] = x[1] - (self.a1[1]+self.a2[1])
        elif near(x[0], self.vv[1,0] + x[1]*self.a2[0]/self.vv[2,1], self.tol): # right boundary
            y[0] = x[0] - self.a1[0]
            y[1] = x[1] - self.a1[1]
        else:   #top boundary
            y[0] = x[0] - self.a2[0]
            y[1] = x[1] - self.a2[1]
            
def get_C_orthotropic(Exx,Eyy,Gxy,nuxy,phase):
    """
    Orthotropic Elastic moduli matrix when given Yound moduli, poisson ratios and Shear moduli
    Args:
        Exx: Young modulus in xx direction
        Eyy: Young modulus in yy direction
        Gxy: Shear modulus in xy direction
        nuxy: Poisson ratio in xy direction
        phase: the phase which we want to calculate the elastic moduli tensor
    Returns:
        orhtotropic elasticity matrix
    """    
    nuyx = (nuxy*Eyy)/Exx
    C = np.array([[Exx/(1-nuxy*nuyx),(nuxy*Eyy)/(1-nuxy*nuyx),0],
              [(nuxy*Eyy)/(1-nuxy*nuyx),Eyy/(1-nuxy*nuyx),0],
              [0,0,Gxy]])
    return as_matrix(C) 

def ortho_from_iso(E,nu):
    """
    Converts isotropic to orthotropic format 
    It is used combined with fet_C_orthotropic for isotropic materials
    Args:
        E: Young modulus
        nu: Poisson ratio
    Returns:
        Exx, Eyy, nu, Gxy : args for get_C_orthotropic
    """   
    Exx = np.array(E)
    Eyy = np.array(E)
    Gxy = np.array(E) / 2. / (1.+np.array(nu))
    return Exx,Eyy,np.array(nu),Gxy

#def get_C_iso(E,nu,phase):#This function was not used
#    '''returns the elasticity matrix for isotropic materials in terms of lambda and mu '''
#    lmbda = E*nu/(1+nu)/(1-2*nu)
#    mu = E/2/(1+nu)
#    C_array = np.array([[lmbda + 2*mu, lmbda, 0],
#                       [lmbda, lmbda + 2*mu, 0],
#                       [0, 0, 2*mu]])
#    return as_matrix(C_array)

def strain(u):
    """
    Gives the strain of a displacement in matrix notation 
    Args:
        u: displacemet 
    Returns:
        srtrain for the displacement (u)
    """
    #return 0.5*(grad(u) + grad(u).T)
    return sym(grad(u))

def strain_Voigt(epsilon):
    """
    Converts the strain from matrix to Voigt notation 
    Args:
        epsilon: strain in matrix notation
    Returns:
        strain epsilon in Voigt notation
    """
    return as_vector([epsilon[0,0],epsilon[1,1],epsilon[0,1]*2])

def stress(stress):
    """
    Converts the stress from Voigt to matrix notation 
    Args:
        stress: stress in Voigt notation
    Returns:
        stress in matrix notation
    """    
    return as_tensor([[stress[0], stress[2]],
                     [stress[2], stress[1]]])

def stress_Voigt(U,Applied_Strain,Exx,Eyy,nuxy,Gxy,phase):
    """
    Stress in Voigt notation given the applied strain and the strain due to displacement u 
    Args:
        U: displacement
        Applied_Strain: strain from load case
        Exx,Eyy,nuxy,Gxy,phase: Young moduli, shear moduli, poisson ratios and phase
    Returns:
        the stress in Voigt notation
    """
    Exx = Exx[phase]
    Eyy = Eyy[phase]
    nuxy = nuxy[phase]
    Gxy = Gxy[phase]
    C = get_C_orthotropic(Exx,Eyy,Gxy,nuxy,phase) #this function considers orthotropic behaviour
    return (dot(C, strain_Voigt(strain(U)+ Applied_Strain)))

def stress_Voigt_generic(U,C,Applied_Strain):
    """
    Stress in Voigt notation if you have the effective elastic moduli  
    Args:
        U: displacement
        C: full elastic moudli tensors
        Applied strain: strain from load case
    Returns:
        the stress in Voigt notation
    """ 
    return (dot(C, strain_Voigt(strain(U)+ Applied_Strain)))

def applied_strain(i):
    """
    Applied strain for the 3 load cases in 11, 22, 12
    Args:
        i: load that identifies the direction of the strain load:
            0: E11, 1: E22, 2: G12
    Returns:
        starain in Voigt notation
    """ 
    Ea = np.zeros((3,))
    Ea[i] = 1
    return np.array([[Ea[0], Ea[2]/2.], 
                    [Ea[2]/2., Ea[1]]])


