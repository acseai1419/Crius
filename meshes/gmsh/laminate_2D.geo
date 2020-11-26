SetFactory("OpenCASCADE");
//Starting with a r of length = 1
Rectangle(1) = {0, 0, 0, 1, 1};
x = 0; y = 0; z = 0; 
//-----------------------------------------------------------------------------------------------------------------------
//Copy in the section below the geometric information generated from the pre-processing module in meshes/txt_mesh/
//The geometric information starts from the first line until
//this line -> s() = BooleanFragments { Surface{1}; Delete; }{ Surface{2:n}; Delete; };
//-----------------------------------------------------------------------------------------------------------------------
Rectangle(2) = {x+0.05, y+0, z+0.0, 0.1,1}; 
Rectangle(3) = {x+0.25, y+0, z+0.0, 0.1,1}; 
Rectangle(4) = {x+0.45, y+0, z+0.0, 0.1,1}; 
Rectangle(5) = {x+0.6499999999999999, y+0, z+0.0, 0.1,1}; 
Rectangle(6) = {x+0.85, y+0, z+0.0, 0.1,1}; 
s() = BooleanFragments { Surface{1}; Delete; }{ Surface{2 :6}; Delete; }; 
//-----------------------------------------------------------------------------------------------------------------------
// STL mesh for bounding boxes:
Geometry.OCCBoundsUseStl = 1;
eps = 1e-5;
//Surfaces in the bounding box of the original box
sin() = Surface In BoundingBox {-eps,-eps,-eps, 1+eps,1+eps,eps};
s() -= sin();
//Deleting the volumes outside the volume of the origina box
Recursive Delete{ Volume{s()}; }
//--------------------------------------------------------------------------------------
//For applying periodic boundaries
//We get all surfaces on the left:
Lxmin() = Line In BoundingBox{-eps, -eps, -eps, +eps, 1+eps, 1+eps};
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
Lymin() = Line In BoundingBox{-eps, -eps, -eps, 1+eps, eps, 1+eps};
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
Physical Surface(1) = {7, 8, 9, 10, 11, 12}; 
Physical Surface(2) = {2, 3, 4, 5, 6}; 
Mesh.CharacteristicLengthMin = 0.07; 
Mesh.CharacteristicLengthMax = 0.07;  
//------------------------------------------------------------------------------------------------------------------------------------------
