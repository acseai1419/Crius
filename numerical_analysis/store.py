import numpy as np
from dolfin import*

def save_mesh(name,mesh,subdomains,meshes_location = "./meshes",paraview_location = "./paraview"):
    File(meshes_location+"/3D/" + name + ".xml") << mesh
    File(paraview_location+"/3D/" + name + "_mesh.pvd") << mesh
    File(meshes_location+"/3D/" + name + "_physical_region.xml") << subdomains
    File(paraview_location+"/3D/" + name + "_physical_region.pvd") << subdomains
    return 0

def save_name(name,results_location="./results"):
    text_file = open(results_location + "/3D/Data/name.txt", "w")
    text_file.write(name)
    text_file.close()

def save_elast_moduli(C,name,results_location="./results"):
    np.savetxt(results_location + "/3D/" + name + "_C.txt", C)

def save_E_nu(name,Exx,Eyy,Ezz,Gxy,Gzx,Gyz,nuxy,nuzx,nuyz,results_location = "./results"):
    np.savetxt(results_location+"/3D/Data/" + name + "_Exx.txt", Exx) 
    np.savetxt(results_location+"/3D/Data/" + name + "_Eyy.txt", Eyy)
    np.savetxt(results_location+"/3D/Data/" + name + "_Ezz.txt", Ezz)
    np.savetxt(results_location+"/3D/Data/" + name + "_Gxy.txt", Gxy)
    np.savetxt(results_location+"/3D/Data/" + name + "_Gzx.txt", Gzx)
    np.savetxt(results_location+"/3D/Data/" + name + "_Gyz.txt", Gyz)
    np.savetxt(results_location+"/3D/Data/" + name + "_nuxy.txt", nuxy)
    np.savetxt(results_location+"/3D/Data/" + name + "_nuzx.txt", nuzx)
    np.savetxt(results_location+"/3D/Data/" + name + "_nuyz.txt", nuyz)

def save_E_nu_iso(name,Exx=None,nuxy=None,results_location = "./results"):
    np.savetxt(results_location+"/3D/Data/" + name + "_E.txt", Exx) 
    np.savetxt(results_location+"/3D/Data/" + name + "_nu.txt", nuxy)
    
def save_Elast_mpi(C_0,C_1,C,name):
    output_file = HDF5File("./results/3D/moduli.h5", "w")
    output_file.write(C_0, "c_0"+name)
    output_file.write(C_1, "c_1"+name)
    output_file.write(C, "C"+name)
    output_file.close()
    
def save_graphs(name,vol_frac,s,C,K_Voigt,K_Reuss,G_Voigt,G_Reuss,K_Mori_Tanaka,G_Mori_Tanaka,K_num,G_num,results_location="./results"):
    file = open(results_location+"/3D/Graphs/{}_{}_{}.txt".format(name,str(int(s)),str(round(vol_frac,2))[2:]),"w")
    file.write("E0/E1 = {} \nvf = {} \n".format(s,vol_frac))
    file.write("K Voigt : {} \n".format(K_Voigt))
    file.write("K Reuss : {} \n".format(K_Reuss))
    file.write("MTK : {} \n".format(K_Mori_Tanaka))
    file.write("FEM_A_K: {} \n".format(K_num))
    file.write("K00  : {} \n".format((C[0,0] + 2 * C[0,1])/3))
    file.write("K11  : {} \n".format((C[1,1] + 2 * C[1,2])/3))
    file.write("K22  : {} \n".format((C[2,2] + 2 * C[2,1])/3))
    file.write("G Voigt : {} \n".format(G_Voigt))
    file.write("G Reuss : {} \n".format(G_Reuss))
    file.write("MTG : {} \n".format(G_Mori_Tanaka))
    file.write("FEM_A_G : {} \n".format(G_num))
    file.write("G33  : {} \n".format((C[3,3])))
    file.write("G44  : {} \n".format((C[4,4])))
    file.write("G55  : {} \n".format((C[5,5])))

    

    











    