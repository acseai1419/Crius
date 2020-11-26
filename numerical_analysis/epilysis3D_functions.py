from dolfin import *
import numpy as np

class PeriodicBoundary(SubDomain):
    def __init__(self, vertices, tolerance=DOLFIN_EPS):
        """ vertices stores the coordinates of the 4 unit cell corners"""
        SubDomain.__init__(self, tolerance)
        self.tol = tolerance
        self.vv = vertices
        self.a1 = self.vv[1,:]-self.vv[0,:] # x
        self.a2 = self.vv[5,:]-self.vv[0,:] # y
        self.a3 = self.vv[3,:]-self.vv[0,:] # z
        
        assert np.linalg.norm((self.vv[7, :]-self.vv[0,:])-(self.vv[5, :]-self.vv[0,:]) - (self.vv[3, :]-self.vv[0,:]) - (self.a1)) <= self.tol
        assert np.linalg.norm((self.vv[7, :]-self.vv[0,:])-(self.vv[1, :]-self.vv[0,:]) - (self.vv[3, :]-self.vv[0,:]) - (self.a2)) <= self.tol
        assert np.linalg.norm((self.vv[7, :]-self.vv[0,:])-(self.vv[1, :]-self.vv[0,:]) - (self.vv[5, :]-self.vv[0,:]) - (self.a3)) <= self.tol

    def inside(self, x, on_boundary):
        return bool((near(x[0], self.vv[0,0], self.tol) or #outter boundary
                     near(x[1], self.vv[0,1], self.tol) or #left boundary
                     near(x[2], self.vv[0,2], self.tol)) and #bottom boundary
                     (not(
                     (near(x[0], self.vv[1,0], self.tol) and near(x[1], self.vv[1,1], self.tol) and near(x[2], self.vv[1,2], self.tol)) or #vertice 1 
                     (near(x[0], self.vv[2,0], self.tol) and near(x[1], self.vv[2,1], self.tol) and near(x[2], self.vv[2,2], self.tol)) or #vertice 2
                     (near(x[0], self.vv[3,0], self.tol) and near(x[1], self.vv[3,1], self.tol) and near(x[2], self.vv[3,2], self.tol)) or #vertice 3
                     (near(x[0], self.vv[4,0], self.tol) and near(x[1], self.vv[4,1], self.tol) and near(x[2], self.vv[4,2], self.tol)) or #vertice 4
                     (near(x[0], self.vv[5,0], self.tol) and near(x[1], self.vv[5,1], self.tol) and near(x[2], self.vv[5,2], self.tol)) or #vertice 5
                     (near(x[0], self.vv[6,0], self.tol) and near(x[1], self.vv[6,1], self.tol) and near(x[2], self.vv[6,2], self.tol)) or #vertice 6
                     (near(x[1], self.vv[2,1], self.tol) and near(x[2], self.vv[2,2], self.tol)) or #line 3-2
                     (near(x[0], self.vv[4,0], self.tol) and near(x[2], self.vv[4,2], self.tol)) or #line 3-4
                     (near(x[0], self.vv[2,0], self.tol) and near(x[1], self.vv[2,1], self.tol)) or #line 1-2
                     (near(x[0], self.vv[4,0], self.tol) and near(x[1], self.vv[4,1], self.tol)) or #line 4-5
                     (near(x[0], self.vv[6,0], self.tol) and near(x[2], self.vv[6,2], self.tol)) or #line 1-6
                     (near(x[1], self.vv[6,1], self.tol) and near(x[2], self.vv[6,2], self.tol))    #line 5-6
                      )) and on_boundary)

    def map(self, x, y):
        if (near(x[0], self.vv[7,0], self.tol) and near(x[1], self.vv[7,1], self.tol) and near(x[2], self.vv[7,2], self.tol)):# if x=a,y=b,z=c
            y[0] = x[0] - (self.a1[0]+self.a2[0]+self.a3[0])
            y[1] = x[1] - (self.a1[1]+self.a2[1]+self.a3[1])
            y[2] = x[2] - (self.a1[2]+self.a2[2]+self.a3[2])
        elif near(x[0],self.vv[7,0],self.tol) and near(x[2],self.vv[7,2],self.tol): #if on top-right line 2-7
            y[0] = x[0] - (self.a1[0]+self.a2[0]+self.a3[0])
            y[1] = x[1]
            y[2] = x[2] - (self.a1[2]+self.a2[2]+self.a3[2])
        elif near(x[1],self.vv[7,1],self.tol) and near(x[2],self.vv[7,2],self.tol): #if on inside top line 4-7
            y[0] = x[0]
            y[1] = x[1] - (self.a1[1]+self.a2[1]+self.a3[1])
            y[2] = x[2] - (self.a1[2]+self.a2[2]+self.a3[2])
        elif near(x[0],self.vv[7,0],self.tol) and near(x[1],self.vv[7,1],self.tol): #if on inside right line 6-7
            y[0] = x[0] - (self.a1[0]+self.a2[0]+self.a3[0])
            y[1] = x[1] - (self.a1[1]+self.a2[1]+self.a3[1])
            y[2] = x[2]
        elif near(x[0], self.vv[1,0], self.tol): # if x=a - right surface
            y[0] = x[0] - (self.a1[0]+self.a2[0]+self.a3[0])
            y[1] = x[1] 
            y[2] = x[2]
        elif near(x[1], self.vv[5,1],self.tol): # if y=b - back surface
            y[0] = x[0]
            y[1] = x[1] - (self.a1[1]+self.a2[1]+self.a3[1])
            y[2] = x[2]
        else: #near(x[2],self.vv[3,2],self.tol): #if z=c - top surface
            y[0] = x[0]
            y[1] = x[1] 
            y[2] = x[2] - (self.a1[2]+self.a2[2]+self.a3[2])
            
def get_C_ortho_inverse(Exx,Eyy,Ezz,Gxy,Gxz,Gyz,nuxy,nuzx,nuyz,phase):
    """This funciton actually implements isotropic since it assumes nuxy = nuyx.
    It is not used since it numerically inverts the matrix while the next 
    function analaytically finds the elasciticy matrix for each phase
    """
    C_inv = np.array([[1/Exx, -nuxy/Exx, -nuzx/Exx, 0., 0., 0.],
                      [-nuxy/Exx, 1/Eyy, -nuyz/Eyy, 0., 0., 0.],
                      [-nuzx/Exx, -nuyz/Eyy, 1/Ezz, 0., 0., 0.],
                      [0., 0., 0., 1/Gyz, 0., 0.],
                      [0., 0., 0., 0., 1/Gxz, 0.],
                      [0., 0., 0., 0., 0., 1/Gxy]])
    C = np.linalg.inv(C_inv)
    return as_matrix(C)

def get_C_orthotropic(Exx,Eyy,Ezz,Gxy,Gzx,Gyz,nuxy,nuzx,nuyz,phase):
    """
    Orthotropic Elastic moduli matrix when given Young moduli, poisson ratios and Shear moduli. C is defined with this function 
    For isotropic and orthotropic materials.
    Args:
        Exx, Eyy, Ezz: Young moduli
        Gxy,Gxz,Gyz: Shear moduli
        nuxy,nuzx,nuyz: Poisson Ratios
        phase: the phase which we want to calculate the elastic moduli tensor
    Returns:
        orhtotropic elasticity matrix
    Reference:
        follows the theory from: https://www.efunda.com/formulae/solid_mechanics/mat_mechanics/hooke_orthotropic.cfm
    """  
    nuyx = (nuxy*Eyy) / Exx
    nuxz = (nuzx*Exx) / Ezz
    nuzy = (nuyz*Ezz) / Eyy
    D = (1 - nuxy*nuyx - nuyz*nuzy - nuzx*nuxz - 2*nuxy*nuyz*nuzx)/(Exx*Eyy*Ezz)
    
    C = np.array([[(1-nuyz*nuzy)/(Eyy*Ezz*D), (nuyx+nuzx*nuyz)/(Eyy*Ezz*D), (nuzx + nuyx*nuzy)/(Eyy*Ezz*D), 0., 0., 0.],
                 [(nuxy+nuxz*nuzy)/(Ezz*Exx*D), (1-nuzx*nuxz)/(Exx*Ezz*D), (nuzy + nuzx*nuxy)/(Exx*Ezz*D), 0., 0., 0.],
                 [(nuxz + nuxy*nuyz)/(Exx*Eyy*D), (nuyz + nuxz*nuyx)/(Exx*Eyy*D), (1-nuxy*nuyx)/(Exx*Eyy*D), 0., 0., 0.],
                 [0., 0., 0., Gyz, 0., 0.],
                 [0., 0., 0., 0., Gzx, 0.],
                 [0., 0., 0., 0., 0., Gxy]])
    return as_matrix(C)

def ortho_from_iso(E,nu):
    """
    Converts isotropic to orthotropic format.
    It is used combined with fet_C_orthotropic for isotropic materials
    Args:
        E: Young modulus
        nu: Poisson ratio
    Returns:
        Exx,Eyy,Ezz,Gxy,Gzx,Gyz,nuxy,nuzx,nuyz
    """
    G = np.array(E) / 2. / (1.+np.array(nu))
    return np.array(E),np.array(E),np.array(E),G,G,G,np.array(nu),np.array(nu),np.array(nu)


def strain(U):
    """
    Gives the strain of a displacement in matrix notation 
    Args:
        u: displacemet 
    Returns:
        srtrain for the displacement (u)
    """
    #return  0.5*(grad(U) + grad(U).T)
    return sym(grad(U))

def strain_Voigt(epsilon):
    """
    Converts the strain from matrix to Voigt notation 
    Args:
        epsilon: strain in matrix notation
    Returns:
        strain epsilon in Voigt notation
    """
#    return as_vector([epsilon[0,0],epsilon[1,1],epsilon[2,2],epsilon[1,2]+epsilon[2,1],epsilon[0,2]+epsilon[2,0],epsilon[0,1]+epsilon[1,0]])
    return as_vector([epsilon[0,0],epsilon[1,1],epsilon[2,2],epsilon[1,2]*2,epsilon[0,2]*2,epsilon[0,1]*2])

def stress(stress):
    """
    Converts the stress from Voigt to matrix notation 
    Args:
        stress: stress in Voigt notation
    Returns:
        stress in matrix notation
    """   
    return as_matrix([[stress[0], stress[5], stress[4]],
                      [stress[5], stress[1], stress[3]],
                      [stress[4], stress[3], stress[2]]])

def stress_Voigt(U,Applied_Strain,Exx,Eyy,Ezz,Gxy,Gzx,Gyz,nuxy,nuzx,nuyz,phase):
    """
    Stress in Voigt notation given the applied strain and the strain due to displacement u 
    Args:
        U: displacement
        Applied_Strain: strain from load case
        E,nu,G,phase: Young moduli, shear moduli, poisson ratios and phase
    Returns:
        the stress in Voigt notation
    """
    Exx = Exx[phase]
    Eyy = Eyy[phase]
    Ezz = Ezz[phase]
    Gxy = Gxy[phase]
    Gzx = Gzx[phase]
    Gyz = Gyz[phase]
    nuxy = nuxy[phase]
    nuzx = nuzx[phase]
    nuyz = nuyz[phase]
    C = get_C_orthotropic(Exx,Eyy,Ezz,Gxy,Gzx,Gyz,nuxy,nuzx,nuyz,phase)
    return (dot(C, strain_Voigt(strain(U)+ Applied_Strain)))

def stress_Voigt_post(U,Exx,Eyy,Ezz,Gxy,Gzx,Gyz,nuxy,nuzx,nuyz,phase):
    """
    Stress in Voigt notation given the the strain due to displacement u - For vtk files
    Args:
        U: displacement
        Applied_Strain: strain from load case
        E,nu,G,phase: Young moduli, shear moduli, poisson ratios and phase
    Returns:
        the stress in Voigt notation
    """
    Exx = Exx[phase]
    Eyy = Eyy[phase]
    Ezz = Ezz[phase]
    Gxy = Gxy[phase]
    Gzx = Gzx[phase]
    Gyz = Gyz[phase]
    nuxy = nuxy[phase]
    nuzx = nuzx[phase]
    nuyz = nuyz[phase]
    C = get_C_orthotropic(Exx,Eyy,Ezz,Gxy,Gzx,Gyz,nuxy,nuzx,nuyz,phase)
    return (dot(C, strain_Voigt(strain(U))))

def stress_Voigt_generic(U,C,Applied_Strain):
    """
    Stress in Voigt notation if the effective moduli is given    
    Args:
        U: displacement
        C: full elastic moudli tensors
        Applied strain: strain from load case
    Returns:
        the stress in Voigt notation
    """ 
    return (dot(C, strain_Voigt(strain(U)+ Applied_Strain)))

def stress_Voigt_generic_num(U,Applied_Strain,C,phase):
    """
    Stress in Voigt notation if you have the full elastic moduli tensors 
    of the submaterials (e.g. for triclinic materials or monoclinic)
    (This is a feuture feature and was not properly tested as it was not in the scope of the research project)    
    Args:
        U: displacement
        C: full elastic moudli tensors
        Applied strain: strain from load case
    Returns:
        the stress in Voigt notation
    """ 
    C = as_matrix(C[phase])
    return (dot(C, strain_Voigt(strain(U)+ Applied_Strain)))

def applied_strain(i):
    """
    Applied strain for the 6 load cases in 11, 22, 33, 23, 31, 12
    Args:
        i: load that identifies the direction of the strain load:
            0: E11, 1: E22, 2: E33, 3:Gyz, 4:Gzx, 5:Gxy
    Returns:
        starain in Voigt notation
    """ 
    Ea_Voigt = np.zeros((6,))
    Ea_Voigt[i] = 1
    return np.array([[Ea_Voigt[0], Ea_Voigt[5]/2.,Ea_Voigt[4]/2.], 
                    [Ea_Voigt[5]/2., Ea_Voigt[1], Ea_Voigt[3]/2.],
                    [Ea_Voigt[4]/2., Ea_Voigt[3]/2., Ea_Voigt[2]]])
