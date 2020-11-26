SetFactory("OpenCASCADE");
//Starting with a box of length = 1
Box(1) = {0, 0, 0, 1, 1, 1};
x = 0; y = 0; z = 0; 
//Copy in the section the geometric information generated from the pre-processing module in meshes/txt_mesh/
//The geometric information starts from the first line until
//this line -> v() = BooleanFragments { Volume{1}; Delete; }{ Volume{2:n}; Delete; };
//-----------------------------------------------------------------------------------------------------------------------
Sphere(2) = {x+0.1, y+0.1, z+0.5, 0.05}; 
Dilate {{ x+0.1, y+0.1, z+0.5},{1,1,8}} {Volume{2}; } 
Sphere(3) = {x+0.1, y+0.3, z+0.5, 0.05}; 
Dilate {{ x+0.1, y+0.3, z+0.5},{1,1,8}} {Volume{3}; } 
Sphere(4) = {x+0.1, y+0.5, z+0.5, 0.05}; 
Dilate {{ x+0.1, y+0.5, z+0.5},{1,1,8}} {Volume{4}; } 
Sphere(5) = {x+0.1, y+0.7, z+0.5, 0.05}; 
Dilate {{ x+0.1, y+0.7, z+0.5},{1,1,8}} {Volume{5}; } 
Sphere(6) = {x+0.1, y+0.9, z+0.5, 0.05}; 
Dilate {{ x+0.1, y+0.9, z+0.5},{1,1,8}} {Volume{6}; } 
Sphere(7) = {x+0.3, y+0.1, z+0.5, 0.05}; 
Dilate {{ x+0.3, y+0.1, z+0.5},{1,1,8}} {Volume{7}; } 
Sphere(8) = {x+0.3, y+0.3, z+0.5, 0.05}; 
Dilate {{ x+0.3, y+0.3, z+0.5},{1,1,8}} {Volume{8}; } 
Sphere(9) = {x+0.3, y+0.5, z+0.5, 0.05}; 
Dilate {{ x+0.3, y+0.5, z+0.5},{1,1,8}} {Volume{9}; } 
Sphere(10) = {x+0.3, y+0.7, z+0.5, 0.05}; 
Dilate {{ x+0.3, y+0.7, z+0.5},{1,1,8}} {Volume{10}; } 
Sphere(11) = {x+0.3, y+0.9, z+0.5, 0.05}; 
Dilate {{ x+0.3, y+0.9, z+0.5},{1,1,8}} {Volume{11}; } 
Sphere(12) = {x+0.5, y+0.1, z+0.5, 0.05}; 
Dilate {{ x+0.5, y+0.1, z+0.5},{1,1,8}} {Volume{12}; } 
Sphere(13) = {x+0.5, y+0.3, z+0.5, 0.05}; 
Dilate {{ x+0.5, y+0.3, z+0.5},{1,1,8}} {Volume{13}; } 
Sphere(14) = {x+0.5, y+0.5, z+0.5, 0.05}; 
Dilate {{ x+0.5, y+0.5, z+0.5},{1,1,8}} {Volume{14}; } 
Sphere(15) = {x+0.5, y+0.7, z+0.5, 0.05}; 
Dilate {{ x+0.5, y+0.7, z+0.5},{1,1,8}} {Volume{15}; } 
Sphere(16) = {x+0.5, y+0.9, z+0.5, 0.05}; 
Dilate {{ x+0.5, y+0.9, z+0.5},{1,1,8}} {Volume{16}; } 
Sphere(17) = {x+0.7, y+0.1, z+0.5, 0.05}; 
Dilate {{ x+0.7, y+0.1, z+0.5},{1,1,8}} {Volume{17}; } 
Sphere(18) = {x+0.7, y+0.3, z+0.5, 0.05}; 
Dilate {{ x+0.7, y+0.3, z+0.5},{1,1,8}} {Volume{18}; } 
Sphere(19) = {x+0.7, y+0.5, z+0.5, 0.05}; 
Dilate {{ x+0.7, y+0.5, z+0.5},{1,1,8}} {Volume{19}; } 
Sphere(20) = {x+0.7, y+0.7, z+0.5, 0.05}; 
Dilate {{ x+0.7, y+0.7, z+0.5},{1,1,8}} {Volume{20}; } 
Sphere(21) = {x+0.7, y+0.9, z+0.5, 0.05}; 
Dilate {{ x+0.7, y+0.9, z+0.5},{1,1,8}} {Volume{21}; } 
Sphere(22) = {x+0.9, y+0.1, z+0.5, 0.05}; 
Dilate {{ x+0.9, y+0.1, z+0.5},{1,1,8}} {Volume{22}; } 
Sphere(23) = {x+0.9, y+0.3, z+0.5, 0.05}; 
Dilate {{ x+0.9, y+0.3, z+0.5},{1,1,8}} {Volume{23}; } 
Sphere(24) = {x+0.9, y+0.5, z+0.5, 0.05}; 
Dilate {{ x+0.9, y+0.5, z+0.5},{1,1,8}} {Volume{24}; } 
Sphere(25) = {x+0.9, y+0.7, z+0.5, 0.05}; 
Dilate {{ x+0.9, y+0.7, z+0.5},{1,1,8}} {Volume{25}; } 
Sphere(26) = {x+0.9, y+0.9, z+0.5, 0.05}; 
Dilate {{ x+0.9, y+0.9, z+0.5},{1,1,8}} {Volume{26}; } 
v() = BooleanFragments { Volume{1}; Delete; }{ Volume{2:26}; Delete; };
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
//In the section below we copy the rest of the information gathered from the file generated from the pre-processing module in meshes/txt_mesh/
//---------------------------------------------------------------------------------------------------------------------------------------
Physical Volume(1) = {27};
Physical Volume(2) = {2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26};
Mesh.CharacteristicLengthMin = 0.02;
Mesh.CharacteristicLengthMax = 0.02;
//------------------------------------------------------------------------------------------------------------------------------------------
