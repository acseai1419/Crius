SetFactory("OpenCASCADE");
//Starting with a box of length = 1
Box(1) = {0, 0, 0, 1, 1, 1};
x = 0; y = 0; z = 0; 
//-----------------------------------------------------------------------------------------------------------------------
//Copy in the section below the geometric information generated from the pre-processing module in meshes/txt_mesh/
//The geometric information starts from the first line until
//this line -> v() = BooleanFragments { Volume{1}; Delete; }{ Volume{2:n}; Delete; };
//-----------------------------------------------------------------------------------------------------------------------
Box(2) = {0, 0, 0, 0.3333333333333333, 0.3333333333333333, 0.3333333333333333}; 
Box(3) = {0.3333333333333333, 0, 0, 0.3333333333333333, 0.3333333333333333, 0.3333333333333333}; 
Box(4) = {0.6666666666666666, 0, 0, 0.3333333333333333, 0.3333333333333333, 0.3333333333333333}; 
Box(5) = {0, 0.3333333333333333, 0, 0.3333333333333333, 0.3333333333333333, 0.3333333333333333}; 
Box(6) = {0.3333333333333333, 0.3333333333333333, 0, 0.3333333333333333, 0.3333333333333333, 0.3333333333333333}; 
Box(7) = {0.6666666666666666, 0.3333333333333333, 0, 0.3333333333333333, 0.3333333333333333, 0.3333333333333333}; 
Box(8) = {0, 0.6666666666666666, 0, 0.3333333333333333, 0.3333333333333333, 0.3333333333333333}; 
Box(9) = {0.3333333333333333, 0.6666666666666666, 0, 0.3333333333333333, 0.3333333333333333, 0.3333333333333333}; 
Box(10) = {0.6666666666666666, 0.6666666666666666, 0, 0.3333333333333333, 0.3333333333333333, 0.3333333333333333}; 
Box(11) = {0, 0, 0.3333333333333333, 0.3333333333333333, 0.3333333333333333, 0.3333333333333333}; 
Box(12) = {0.3333333333333333, 0, 0.3333333333333333, 0.3333333333333333, 0.3333333333333333, 0.3333333333333333}; 
Box(13) = {0.6666666666666666, 0, 0.3333333333333333, 0.3333333333333333, 0.3333333333333333, 0.3333333333333333}; 
Box(14) = {0, 0.3333333333333333, 0.3333333333333333, 0.3333333333333333, 0.3333333333333333, 0.3333333333333333}; 
Box(15) = {0.3333333333333333, 0.3333333333333333, 0.3333333333333333, 0.3333333333333333, 0.3333333333333333, 0.3333333333333333}; 
Box(16) = {0.6666666666666666, 0.3333333333333333, 0.3333333333333333, 0.3333333333333333, 0.3333333333333333, 0.3333333333333333}; 
Box(17) = {0, 0.6666666666666666, 0.3333333333333333, 0.3333333333333333, 0.3333333333333333, 0.3333333333333333}; 
Box(18) = {0.3333333333333333, 0.6666666666666666, 0.3333333333333333, 0.3333333333333333, 0.3333333333333333, 0.3333333333333333}; 
Box(19) = {0.6666666666666666, 0.6666666666666666, 0.3333333333333333, 0.3333333333333333, 0.3333333333333333, 0.3333333333333333}; 
Box(20) = {0, 0, 0.6666666666666666, 0.3333333333333333, 0.3333333333333333, 0.3333333333333333}; 
Box(21) = {0.3333333333333333, 0, 0.6666666666666666, 0.3333333333333333, 0.3333333333333333, 0.3333333333333333}; 
Box(22) = {0.6666666666666666, 0, 0.6666666666666666, 0.3333333333333333, 0.3333333333333333, 0.3333333333333333}; 
Box(23) = {0, 0.3333333333333333, 0.6666666666666666, 0.3333333333333333, 0.3333333333333333, 0.3333333333333333}; 
Box(24) = {0.3333333333333333, 0.3333333333333333, 0.6666666666666666, 0.3333333333333333, 0.3333333333333333, 0.3333333333333333}; 
Box(25) = {0.6666666666666666, 0.3333333333333333, 0.6666666666666666, 0.3333333333333333, 0.3333333333333333, 0.3333333333333333}; 
Box(26) = {0, 0.6666666666666666, 0.6666666666666666, 0.3333333333333333, 0.3333333333333333, 0.3333333333333333}; 
Box(27) = {0.3333333333333333, 0.6666666666666666, 0.6666666666666666, 0.3333333333333333, 0.3333333333333333, 0.3333333333333333}; 
Box(28) = {0.6666666666666666, 0.6666666666666666, 0.6666666666666666, 0.3333333333333333, 0.3333333333333333, 0.3333333333333333}; 
v() = BooleanFragments { Volume{1}; Delete; }{ Volume{2 :28}; Delete; }; 
//-----------------------------------------------------------------------------------------------------------------------
// STL mesh for bounding boxes:
Geometry.OCCBoundsUseStl = 1;
eps = 1e-3;
//volumes in the bounding box of the original box
vin() = Volume In BoundingBox {-eps,-eps,-eps, 1+eps,1+eps,1+eps};
v() -= vin();
//Deleting the volumes outside the volume of the origina box
Recursive Delete{ Volume{v()}; }
//--------------------------------------------------------------------------------------
//For applying periodic boundaries
//We get all surfaces on the left:
Sxmin() = Surface In BoundingBox{-eps, -eps, -eps, +eps, 1+eps, 1+eps};
For i In {0:#Sxmin()-1}
  // We get the bounding box of the left surfaces
  bb() = BoundingBox Surface { Sxmin(i) };
  // We translate the bounding box to the right and look for surfaces inside i
  Sxmax() = Surface In BoundingBox { bb(0)-eps+1, bb(1)-eps, bb(2)-eps,
                                     bb(3)+eps+1, bb(4)+eps, bb(5)+eps };
  // For all the matches, we compare the corresponding bounding boxes
  For j In {0:#Sxmax()-1}
    bb2() = BoundingBox Surface { Sxmax(j) };
    bb2(0) -= 1;
    bb2(3) -= 1;
    // if they match, we apply the periodicity constraint
    If(Fabs(bb2(0)-bb(0)) < eps && Fabs(bb2(1)-bb(1)) < eps &&
       Fabs(bb2(2)-bb(2)) < eps && Fabs(bb2(3)-bb(3)) < eps &&
       Fabs(bb2(4)-bb(4)) < eps && Fabs(bb2(5)-bb(5)) < eps)
      Periodic Surface {Sxmax(j)} = {Sxmin(i)} Translate {1,0,0};
    EndIf
  EndFor
EndFor

//We get all surfaces on the outside:
Symin() = Surface In BoundingBox{-eps, -eps, -eps, 1+eps, eps, 1+eps};
For i In {0:#Symin()-1}
  // We get the bounding box of each outter surface
  bb() = BoundingBox Surface { Symin(i) };
  // We translate the bounding box to the inside and look for surfaces inside i
  Symax() = Surface In BoundingBox { bb(0)-eps, bb(1)-eps+1, bb(2)-eps,
                                     bb(3)+eps, bb(4)+eps+1, bb(5)+eps };
  // For all the matches, we compare the corresponding bounding boxes
  For j In {0:#Symax()-1}
    bb2() = BoundingBox Surface { Symax(j) };
    bb2(1) -= 1;
    bb2(4) -= 1;
    // if they match, we apply the periodicity constraint
    If(Fabs(bb2(0)-bb(0)) < eps && Fabs(bb2(1)-bb(1)) < eps &&
       Fabs(bb2(2)-bb(2)) < eps && Fabs(bb2(3)-bb(3)) < eps &&
       Fabs(bb2(4)-bb(4)) < eps && Fabs(bb2(5)-bb(5)) < eps)
      Periodic Surface {Symax(j)} = {Symin(i)} Translate {0,1,0};
    EndIf
  EndFor
EndFor

// We get all surfaces on the bottom:
Szmin() = Surface In BoundingBox{-eps, -eps, -eps, 1+eps, 1+eps, +eps};

For i In {0:#Szmin()-1}
  // We get the bounding box of each bottom surface
  bb() = BoundingBox Surface { Szmin(i) };
  // We translate the bounding box to the top and look for surfaces inside i
  Szmax() = Surface In BoundingBox { bb(0)-eps, bb(1)-eps, bb(2)-eps+1,
                                     bb(3)+eps, bb(4)+eps, bb(5)+eps+1 };
  // For all the matches, we compare the corresponding bounding boxes
  For j In {0:#Szmax()-1}
    bb2() = BoundingBox Surface { Szmax(j) };
    bb2(2) -= 1;
    bb2(5) -= 1;
    // ...and if they match, we apply the periodicity constraint
    If(Fabs(bb2(0)-bb(0)) < eps && Fabs(bb2(1)-bb(1)) < eps &&
       Fabs(bb2(2)-bb(2)) < eps && Fabs(bb2(3)-bb(3)) < eps &&
       Fabs(bb2(4)-bb(4)) < eps && Fabs(bb2(5)-bb(5)) < eps)
      Periodic Surface {Szmax(j)} = {Szmin(i)} Translate {0,0,1};
    EndIf
  EndFor
EndFor
//---------------------------------------------------------------------------------------------------------------------------------------
//In this section we copy the rest of the information gathered from the file generated from the pre-processing module in meshes/txt_mesh/
//---------------------------------------------------------------------------------------------------------------------------------------
Physical Volume(1) = {3, 8, 12, 16, 18}; 
Physical Volume(2) = {4, 5, 11, 17, 19, 22, 24, 26, 28}; 
Physical Volume(3) = {7, 9, 10, 15, 23, 25, 27}; 
Physical Volume(4) = {2, 6, 13, 14, 20, 21}; 
Mesh.CharacteristicLengthMin = 0.3333333333333333; 
Mesh.CharacteristicLengthMax = 0.3333333333333333;
//------------------------------------------------------------------------------------------------------------------------------------------
