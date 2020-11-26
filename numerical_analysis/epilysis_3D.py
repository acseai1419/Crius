import numpy as np
from fenics import *
import store
from epilysis3D_functions import PeriodicBoundary, strain, strain_Voigt, stress, stress_Voigt, applied_strain, stress_Voigt_generic, stress_Voigt_generic_num, stress_Voigt_post

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
    Volume_fraction = assemble(1*dx(2)) / assemble(1*dx)
    return Volume_fraction

def fe_problem(mesh,subdomains,vertices,Exx=None,Eyy=None,Ezz=None,Gxy=None,Gzx=None,Gyz=None,nuxy=None,nuzx=None,nuyz=None,tol = 1e-15,C_gen=None,):
    """
    Sets up the elastic problem 
    Args:
        mesh
        subdomains
        vertices: vertices of the rectangle
        E,G,nu: Young moduli, Shear moduli, Poisson ratios
        tol: tolerance for periodicity
    The following settings are available with commenting uncommenting:
        (iii) Full elasticity matrix instead of young moduli and poisson ratio (not tested/feature work)
        (iii) This is a feuture feature and was not properly tested as it was not in the scope of the research project
    Returns:
        dx for each subdomain, w: variable of interest, Ea:applied strain, F:equation, a: LHS, L:RHS
    Followes the theory from the report
    Reference:
       Bleyer, J., 2018. Numerical tours of continuum mechanics using FEniCS
    """
    if type(Exx) == np.ndarray:
        phases = len(Exx)
    if type(C_gen) == np.ndarray:
        phases = np.shape(C_gen)[0]
    dx = Measure('dx', domain=mesh, subdomain_data=subdomains) #dx for the subdomains
    Volume_fraction = assemble(1*dx(2)) / assemble(1*dx)  #
    Ve = VectorElement("CG", mesh.ufl_cell(), 2)  
    Re = VectorElement("R", mesh.ufl_cell(), 0) #langrange multiplier
    W = FunctionSpace(mesh, MixedElement([Ve, Re]), constrained_domain=PeriodicBoundary(vertices, tolerance=tol))
    
    v_,lamb_ = TestFunctions(W)
    dv, dlamb = TrialFunctions(W)
    w = Function(W)
    
    Ea = Constant(((0,0,0),(0,0,0),(0,0,0)))
    #-----------------------------------------------------------------------------------------------------------------------------------------------
    F = sum([inner(stress(stress_Voigt(dv, Ea,Exx,Eyy,Ezz,Gxy,Gzx,Gyz,nuxy,nuzx,nuyz,i)), strain(v_))*dx(i+1) for i in range (phases)]) #(iii)
    #F = sum([inner(stress(stress_Voigt_generic_num(dv,Ea,C_gen,i)), strain(v_))*dx(i+1) for i in range (phases)]) #This is for general C matrices(iii)
    #-----------------------------------------------------------------------------------------------------------------------------------------------
    a, L = lhs(F), rhs(F)
    a += dot(lamb_,dv)*dx + dot(dlamb,v_)*dx
    return dx,w,Ea,F,a,L

def calculate_moduli(name,mesh,vol,dx,w,Ea,F,a,L,Exx=None,Eyy=None,Ezz=None,Gxy=None,Gzx=None,Gyz=None,nuxy=None,nuzx=None,nuyz=None,mesh_location="./meshes",paraview_location="./paraview",results_location="./results",C_gen=None,):
    """
    Calculates effective elastic modui and saves paraview files with microscopic stress and strain 
    Args:
        name
        mesh
        vol: a*b*c
        dx,w,Ea,F,a,L: from fe_problem
        E,nu,G: moduli
        locations: location for which running the code from
    The following settings are available with commenting uncommenting:
        (i) solver parameters
        (ii) exporting stess/displacement fields with .vtk files
        (iii) Full elasticity matrix instead of young moduli and poisson ratio (not tested/feature work)
        (iii) This is a feuture feature and was not properly tested as it was not in the scope of the research project
    Returns:
        effective moduli
    Followes the theory from the report
    Reference:
       Bleyer, J., 2018. Numerical tours of continuum mechanics using FEniCS
    """
    if type(Exx) == np.ndarray:
        phases = len(Exx)
    if type(C_gen) == np.ndarray:
        phases = np.shape(C_gen)[0]
    C_guess = np.zeros((6,6))
    for i in range(6):
        print("Solving linear problem ...")
        Ea.assign(Constant(applied_strain(i)))
        #--------------------------------------------------------------------------------------------------------
        #(i) #default and only option for MPI 
        solve(a == L, w, [], solver_parameters={"linear_solver": "gmres"})
        #--------------------------------------------------------------------------------------------------------
        #This section is allowing to change the parameters of the solver. 
        #(i) #default for serial
        #uncomment and comment the other solver if change tha parameters are needed
#        problem = LinearVariationalProblem(a, L, w, [])
#        solver = LinearVariationalSolver(problem)
#        solver.parameters['linear_solver'] = 'gmres'
#        solver.parameters['preconditioner'] = 'ilu'
#        prm = solver.parameters['krylov_solver']
#        prm['absolute_tolerance'] = 1E-8
#        prm['relative_tolerance'] = 1E-4
#        prm['maximum_iterations'] = 20000
#        solver.solve()
        #-------------------------------------------------------------------------------------------------------------
        v, lamb = w.split()
        #-------------------------------------------------------------------------------------------------------------
#       #Uncomment this section if vtk files are needed (ii)
#        vtkfile = File(paraview_location+'/3D'+'/displacement_'+name+str(i)+'.pvd')
#        vtkfile << v
#        vtk_stress = File(paraview_location+'/3D'+'/stress_'+name+str(i)+'.pvd')
#        s_v = as_vector(np.zeros((6,)))
#        for l in range(len(Exx)):
#            s_v += stress_Voigt_post(v,Exx,Eyy,Ezz,Gxy,Gzx,Gyz,nuxy,nuzx,nuyz,l)
#        vtk_stress << project(stress(s_v), TensorFunctionSpace(mesh, 'CG', 1),solver_type="gmres")
        #--------------------------------------------------------------------------------------------------------------
        output_file = HDF5File(mesh.mpi_comm(), results_location+"/3D/V/v.h5"+str(i), "w")  # Saves the solution
        output_file.write(v, "solution_"+name+str(i))
        output_file.close()
        Stress_a = np.zeros((6,))
        for k in range(6):
            for j in range(phases):
                Stress_a[k] += assemble((stress_Voigt(v,Ea,Exx,Eyy,Ezz,Gxy,Gzx,Gyz,nuxy,nuzx,nuyz,j))[k]*dx(j+1)) / vol #(iii)
                #Stress_a[k] += assemble((stress_Voigt_generic_num(v,Ea,C_gen,j))[k]*dx(j+1)) / vol #This is when provided with full C matrices instead of E,nu (iii)             
        C_guess[i,:] += Stress_a
    store.save_elast_moduli(C_guess,name,results_location)
    return C_guess
