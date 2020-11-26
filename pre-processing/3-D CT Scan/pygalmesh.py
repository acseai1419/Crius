import numpy as np
from PIL import Image
import pygalmesh
nz=300
nx=955
ny=1114
gray=np.zeros((nx,ny,nz))
for k in range(nz):
    seq='{:04d}'.format(k)
    #print(seq)
    filename = "Tiffs/KS21Bin"+seq+".tif"
    #print(filename)
    im = Image.open(filename)
    gray[:,:,k] = np.array(im)
gray=gray/np.max(gray)
subset=gray[0:300,0:300,0:300]
nx = 300
ny = 300
nz = 300
h = [30] * 3
vol = subset.astype(np.uint8)
mesh = pygalmesh.generate_from_array(vol, h, max_facet_distance=15)
mesh.write("pygalmesh_solid_30_15.vtk")
mesh.write("pygalmesh_solid_30_15.stl")
