SetFactory("OpenCASCADE");
//Starting with a r of length = 1
Rectangle(1) = {0, 0, 0, 1, 1};
x = 0; y = 0; z = 0; 
//-----------------------------------------------------------------------------------------------------------------------
//Copy in the section below the geometric information generated from the pre-processing module in meshes/txt_mesh/
//The geometric information starts from the first line until
//this line -> s() = BooleanFragments { Surface{1}; Delete; }{ Surface{2:n}; Delete; };
//-----------------------------------------------------------------------------------------------------------------------
Disk(2) = {x+0.8405369311050865, y+0.21744629588692205, z+0.0, 0.14742620240508925}; 
Disk(3) = {x+0.5689269936703258, y+0.7108321490408989, z+0.0, 0.12191463607628719}; 
Disk(4) = {x+0.1437302763505147, y+0.6520849995303816, z+0.0, 0.13136959265368878}; 
Disk(5) = {x+0.3788693557415097, y+0.43395233126686295, z+0.0, 0.1277132975497042}; 
Disk(6) = {x+0.13605765008334836, y+0.20603274613263756, z+0.0, 0.10821782268557797}; 
Disk(7) = {x+0.8179244865780376, y+0.6338013757857066, z+0.0, 0.13563392729432608}; 
Disk(8) = {x+0.56700348790972, y+0.1891932860729879, z+0.0, 0.1244051298721262}; 
Disk(9) = {x+0.344260051728317, y+0.8780797155052952, z+0.0, 0.10567715754503604}; 
s() = BooleanFragments { Surface{1}; Delete; }{ Surface{2 :9}; Delete; }; 
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
Physical Surface(0) = {10}; 
Physical Surface(1) = {2, 3, 4, 5, 6, 7, 8, 9}; 
Mesh.CharacteristicLengthMin = 0.05; 
Mesh.CharacteristicLengthMax = 0.05; 
//------------------------------------------------------------------------------------------------------------------------------------------
