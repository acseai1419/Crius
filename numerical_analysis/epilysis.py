import numpy as np
from fenics import *
from epilysis_functions import PeriodicBoundary,strain,strain_Voigt,stress,stress_Voigt,applied_strain,stress_Voigt_generic
import i_o

def calculate_Volume_fraction(mesh,subdomains):
    """
    Calculates the Volume_fraction of the second phase 
    Args:
        mesh,
        subdomains
    Returns:
        Volume_fraction
    """
    dx = Measure('dx', domain=mesh, subdomain_data=subdomains)
    # Computing the volume fraction of phase (1)->second phase
    Volume_fraction = assemble(1*dx(1)) / assemble(1*dx)
    return Volume_fraction
    
def fe_problem(mesh,subdomains,vertices,area,Exx=None,Eyy=None,nuxy=None,Gxy=None,tol = 1e-15):
    """
    Sets up the elastic problem 
    Args:
        mesh
        subdomains
        vertices: vertices of the rectangle
        area: a*b
        Exx,Eyy,nuxy,Gxy: moduli
        tol: tolerance for periodicity
    Returns:
        dx for each subdomain, w: variable of interest, Ea:applied strain, F:equation, a: LHS, L:RHS
    Followes the theory from the report
    Reference:
       Bleyer, J., 2018. Numerical tours of continuum mechanics using FEniCS
    """
    dx = Measure('dx', domain=mesh, subdomain_data=subdomains) #dx for the subdomains
    Ve = VectorElement("CG", mesh.ufl_cell(), 2)
    Re = VectorElement("R", mesh.ufl_cell(), 0) #langrange multiplier
    W = FunctionSpace(mesh, MixedElement([Ve, Re]), constrained_domain=PeriodicBoundary(vertices, tolerance=tol))#adding the periodic boundary class to the function space
    
    v_,lamb_ = TestFunctions(W)
    dv, dlamb = TrialFunctions(W)
    w = Function(W)
    
    Ea = Constant(((0, 0), (0, 0))) #applied strain
    F = inner(stress(stress_Voigt(dv,Ea,Exx,Eyy,nuxy,Gxy,0)), strain(v_))*dx(0) + inner(stress(stress_Voigt(dv,Ea,Exx,Eyy,nuxy,Gxy,1)), strain(v_))*dx(1) #equation

    a, L = lhs(F), rhs(F)
    a += dot(lamb_,dv)*dx + dot(dlamb,v_)*dx #adding the terms from the langrage multipliers on the left hand side
    return dx,w,Ea,F,a,L

def calculate_moduli(name,mesh,area,dx,w,Ea,F,a,L,Exx=None,Eyy=None,nuxy=None,Gxy=None,meshes_location="./meshes",paraview_location="./paraview",results_location="./results"):
    """
    Calculates effective elastic modui and saves paraview files with microscopic stress and displacement fields 
    Args:
        name
        mesh
        area: a*b
        dx,w,Ea,F,a,L: from fe_problem
        Exx,Eyy,nuxy,Gxy: moduli
        locations: location for which running the code from
    Returns:
        effective moduli
    Followes the theory from the report
    Reference:
       Bleyer, J., 2018. Numerical tours of continuum mechanics using FEniCS
    """
    C_guess_0 = np.zeros((3,3)) 
    C_guess_1 = np.zeros((3,3)) 
    for i in range (3):#for the 3 load cases in the 2-D case
        Ea.assign(Constant(applied_strain(i)))
        solve(a == L, w, [], solver_parameters={'linear_solver': 'cg',
                                             'preconditioner': 'default'},
                                            form_compiler_parameters={"optimize": True})
        v, lamb = w.split()
        #Uncomment the section below if you need to save paraview files
        #---------------------------------------------------------------------------------------------------------------------------------------
#        vtkfile = File(paraview_location+'/2D'+'/displacement_'+name+str(i)+'.pvd')
#        vtkfile << v
#        vtk_stress = File(paraview_location+'/2D'+'/stress_'+name+str(i)+'.pvd')
#        vtk_stress << project(stress(stress_Voigt(v,Ea,Exx,Eyy,nuxy,Gxy,0)+stress_Voigt(v,Ea,Exx,Eyy,nuxy,Gxy,1)), TensorFunctionSpace(mesh, 'CG', 1))
        #----------------------------------------------------------------------------------------------------------------------------------------
        # Save solution
        output_file = HDF5File(mesh.mpi_comm(), results_location+"/2D/V/v.h5"+str(i), "w")
        output_file.write(v, "solution_"+name+str(i))
        output_file.close()
        Stress_0 = np.zeros((3,))
        Stress_1 = np.zeros((3,))
        for k in range(3):
            Stress_0[k] = assemble((stress_Voigt(v,Ea,Exx,Eyy,nuxy,Gxy,0))[k]*dx(0)) / area
            Stress_1[k] = assemble((stress_Voigt(v,Ea,Exx,Eyy,nuxy,Gxy,1))[k]*dx(1)) / area
        C_guess_0[i, :] = Stress_0
        C_guess_1[i, :] = Stress_1
    C_guess = C_guess_0 + C_guess_1
    i_o.save_elast_moduli(C_guess,C_guess_0,C_guess_1,name,results_location)
    i_o.save_E_nu(name,Exx,Eyy,nuxy,Gxy,results_location)
    return C_guess