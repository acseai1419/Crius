SetFactory("OpenCASCADE");
//Starting with a r of length = 1
Rectangle(1) = {0, 0, 0, 1, 1};
x = 0; y = 0; z = 0; 
//-----------------------------------------------------------------------------------------------------------------------
//Copy in the section below the geometric information generated from the pre-processing module in meshes/txt_mesh/
//The geometric information starts from the first line until
//this line -> s() = BooleanFragments { Surface{1}; Delete; }{ Surface{2:n}; Delete; };
//-----------------------------------------------------------------------------------------------------------------------
Disk(2) = {x+0.15842989300627308, y+0.44329710993931115, z+0.0, 0.13567198151461446}; 
Disk(3) = {x+0.8584183638388054, y+0.1602203198026224, z+0.0, 0.13595444970968204}; 
Disk(4) = {x+0.5197884882663959, y+0.8411706831722501, z+0.0, 0.1279907296520409}; 
Disk(5) = {x+0.989665891874833, y+0.8796282968334426, z+0.0, 0.14391945274285722}; 
Disk(6) = {x+-0.010334108125166996, y+-0.12037170316655743, z+0.0, 0.14391945274285722}; 
Disk(7) = {x+0.989665891874833, y+-0.12037170316655743, z+0.0, 0.14391945274285722}; 
Disk(8) = {x+-0.010334108125166996, y+0.8796282968334426, z+0.0, 0.14391945274285722}; 
Disk(9) = {x+0.5521367242218799, y+0.0696743607082364, z+0.0, 0.1107687835940349}; 
Disk(10) = {x+0.5521367242218799, y+1.0696743607082364, z+0.0, 0.1107687835940349}; 
Disk(11) = {x+0.36570915309792906, y+0.24984766012030202, z+0.0, 0.11769918752057515}; 
Disk(12) = {x+0.6989299056350962, y+0.588384704415619, z+0.0, 0.12918342375476383}; 
Disk(13) = {x+0.44580286095097443, y+0.5518408237802421, z+0.0, 0.10016345994775112};  
s() = BooleanFragments { Surface{1}; Delete; }{ Surface{2 :13}; Delete; }; 
//-----------------------------------------------------------------------------------------------------------------------
// STL mesh for bounding boxes:
Geometry.OCCBoundsUseStl = 1;
eps = 1e-3;
//Surfaces in the bounding box of the original box
sin() = Surface In BoundingBox {-eps,-eps,-eps, 1+eps,1+eps,eps};
s() -= sin();
//Deleting the volumes outside the volume of the origina box
Recursive Delete{ Surface{s()}; }
//--------------------------------------------------------------------------------------
//For applying periodic boundaries
//We get all surfaces on the left:
Lxmin() = Line In BoundingBox{-eps, -eps, -eps, +eps, 1+eps, -eps};
For i In {0:#Lxmin()-1}
  // Then we get the bounding box of each left surface
  bb() = BoundingBox Line { Lxmin(i) };
  // We translate the bounding box to the right and look for surfaces inside i
  Lxmax() = Line In BoundingBox { bb(0)-eps+1, bb(1)-eps, bb(2)-eps,
                                     bb(3)+eps+1, bb(4)+eps, bb(5)+eps };
  // For all the matches, we compare the corresponding bounding boxes
  For j In {0:#Lxmax()-1}
    bb2() = BoundingBox Line { Lxmax(j) };
    bb2(0) -= 1;
    bb2(3) -= 1;
    // ...and if they match, we apply the periodicity constraint
    If(Fabs(bb2(0)-bb(0)) < eps && Fabs(bb2(1)-bb(1)) < eps &&
       Fabs(bb2(2)-bb(2)) < eps && Fabs(bb2(3)-bb(3)) < eps &&
       Fabs(bb2(4)-bb(4)) < eps && Fabs(bb2(5)-bb(5)) < eps)
      Periodic Line {Lxmax(j)} = {Lxmin(i)} Translate {1,0,0};
    EndIf
  EndFor
EndFor

// We get all surfaces on the bottom:
Lymin() = Line In BoundingBox{-eps, -eps, -eps, 1+eps, eps, -eps};
For i In {0:#Lymin()-1}
  // Then we get the bounding box of each outter surface
  bb() = BoundingBox Line { Lymin(i) };
  // We translate the bounding box to the top and look for surfaces inside i
  Lymax() = Line In BoundingBox { bb(0)-eps, bb(1)-eps+1, bb(2)-eps,
                                     bb(3)+eps, bb(4)+eps+1, bb(5)+eps };
  // For all the matches, we compare the corresponding bounding boxes...
  For j In {0:#Lymax()-1}
    bb2() = BoundingBox Line { Lymax(j) };
    bb2(1) -= 1;
    bb2(4) -= 1;
    // ...and if they match, we apply the periodicity constraint
    If(Fabs(bb2(0)-bb(0)) < eps && Fabs(bb2(1)-bb(1)) < eps &&
       Fabs(bb2(2)-bb(2)) < eps && Fabs(bb2(3)-bb(3)) < eps &&
       Fabs(bb2(4)-bb(4)) < eps && Fabs(bb2(5)-bb(5)) < eps)
      Periodic Line {Lymax(j)} = {Lymin(i)} Translate {0,1,0};
    EndIf
  EndFor
EndFor
//---------------------------------------------------------------------------------------------------------------------------------------
//In this section we copy the rest of the information gathered from the file generated from the pre-processing module in meshes/txt_mesh/
//---------------------------------------------------------------------------------------------------------------------------------------
//In this periodic case the physical regions are set manually by observing the surfaces in Gmsh software interface
Physical Surface(0) = {15}; 
Physical Surface(1) = {2, 3, 11, 12, 13, 14, 16, 17, 18, 19, 20, 21, 22}; 
Mesh.CharacteristicLengthMin = 0.05; 
Mesh.CharacteristicLengthMax = 0.05;
//------------------------------------------------------------------------------------------------------------------------------------------
