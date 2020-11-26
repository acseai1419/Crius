SetFactory("OpenCASCADE");
// We start with a cube and some spheres:
Box(1) = {0, 0, 0, 1, 1, 1};
x = 0; y = 0; z = 0; 
Box(2) = {x+0.02500000000000001, y, z, 0.15, 1, 1 }; 
Box(3) = {x+0.22499999999999998, y, z, 0.15, 1, 1 }; 
Box(4) = {x+0.425, y, z, 0.15, 1, 1 }; 
Box(5) = {x+0.625, y, z, 0.15, 1, 1 }; 
Box(6) = {x+0.8250000000000001, y, z, 0.15, 1, 1 };
v() = BooleanFragments { Volume{1}; Delete; }{ Volume{2 :6}; Delete; };
 
// Ask OpenCASCADE to compute more accurate bounding boxes of entities using the
// STL mesh:
Geometry.OCCBoundsUseStl = 1;

// We then retrieve all the volumes in the bounding box of the original cube,
// and delete all the parts outside it:
eps = 1e-3;
vin() = Volume In BoundingBox {-eps,-eps,-eps, 1+eps,1+eps,1+eps};
v() -= vin();
Recursive Delete{ Volume{v()}; }

// First we get all surfaces on the left:
Sxmin() = Surface In BoundingBox{-eps, -eps, -eps, +eps, 1+eps, 1+eps};

For i In {0:#Sxmin()-1}
  // Then we get the bounding box of each left surface
  bb() = BoundingBox Surface { Sxmin(i) };
  // We translate the bounding box to the right and look for surfaces inside i
  Sxmax() = Surface In BoundingBox { bb(0)-eps+1, bb(1)-eps, bb(2)-eps,
                                     bb(3)+eps+1, bb(4)+eps, bb(5)+eps };
  // For all the matches, we compare the corresponding bounding boxes...
  For j In {0:#Sxmax()-1}
    bb2() = BoundingBox Surface { Sxmax(j) };
    bb2(0) -= 1;
    bb2(3) -= 1;
    // ...and if they match, we apply the periodicity constraint
    If(Fabs(bb2(0)-bb(0)) < eps && Fabs(bb2(1)-bb(1)) < eps &&
       Fabs(bb2(2)-bb(2)) < eps && Fabs(bb2(3)-bb(3)) < eps &&
       Fabs(bb2(4)-bb(4)) < eps && Fabs(bb2(5)-bb(5)) < eps)
      Periodic Surface {Sxmax(j)} = {Sxmin(i)} Translate {1,0,0};
    EndIf
  EndFor
EndFor

// Then we get all surfaces on the outter:
Symin() = Surface In BoundingBox{-eps, -eps, -eps, 1+eps, eps, 1+eps};

For i In {0:#Symin()-1}
  // Then we get the bounding box of each outter surface
  bb() = BoundingBox Surface { Symin(i) };
  // We translate the bounding box to the right and look for surfaces inside i
  Symax() = Surface In BoundingBox { bb(0)-eps, bb(1)-eps+1, bb(2)-eps,
                                     bb(3)+eps, bb(4)+eps+1, bb(5)+eps };
  // For all the matches, we compare the corresponding bounding boxes...
  For j In {0:#Symax()-1}
    bb2() = BoundingBox Surface { Symax(j) };
    bb2(1) -= 1;
    bb2(4) -= 1;
    // ...and if they match, we apply the periodicity constraint
    If(Fabs(bb2(0)-bb(0)) < eps && Fabs(bb2(1)-bb(1)) < eps &&
       Fabs(bb2(2)-bb(2)) < eps && Fabs(bb2(3)-bb(3)) < eps &&
       Fabs(bb2(4)-bb(4)) < eps && Fabs(bb2(5)-bb(5)) < eps)
      Periodic Surface {Symax(j)} = {Symin(i)} Translate {0,1,0};
    EndIf
  EndFor
EndFor

// Then we get all surfaces on the bottom:
Szmin() = Surface In BoundingBox{-eps, -eps, -eps, 1+eps, 1+eps, +eps};

For i In {0:#Szmin()-1}
  // Then we get the bounding box of each left surface
  bb() = BoundingBox Surface { Szmin(i) };
  // We translate the bounding box to the right and look for surfaces inside i
  Szmax() = Surface In BoundingBox { bb(0)-eps, bb(1)-eps, bb(2)-eps+1,
                                     bb(3)+eps, bb(4)+eps, bb(5)+eps+1 };
  // For all the matches, we compare the corresponding bounding boxes...
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

Physical Volume(1) = {7, 8, 9, 10, 11, 12}; 
Physical Volume(2) = {2, 3, 4, 5, 6}; 
Mesh.CharacteristicLengthMin = 0.25; 
Mesh.CharacteristicLengthMax = 0.25; 
