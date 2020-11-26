SetFactory("OpenCASCADE");
Mesh.CharacteristicLengthMin = 0.09;
Mesh.CharacteristicLengthMax = 0.09;
// We start with a cube and some spheres:
Box(1) = {0, 0, 0, 1, 1, 1};
x = 0; y = 0; z = 0;
Sphere(2) = {x, y, z, 0.3};
Sphere(3) = {x+1, y, z, 0.3};
Sphere(4) = {x, y+1, z, 0.3};
Sphere(5) = {x, y, z+1, 0.3};
Sphere(6) = {x+1, y+1, z, 0.3};
Sphere(7) = {x, y+1, z+1, 0.3};
Sphere(8) = {x+1, y, z+1, 0.3};
Sphere(9) = {x+1, y+1, z+1, 0.3};
Sphere(10) = {x+0.47435772918568486, y+0.3925787129064767, z+0.4877165794960545, 0.1}; 
Sphere(11) = {x+0.44858612188316727, y+0.616557622483306, z+0.4792212164681876, 0.1}; 
Sphere(12) = {x+0.6202779869556516, y+0.4283557928839945, z+0.30749816145226355, 0.1}; 
Sphere(13) = {x+0.6794938629246008, y+0.3577320065275262, z+0.6459149811775806, 0.1}; 
Sphere(14) = {x+0.6466538993155594, y+0.5783597452049083, z+0.5371289275009635, 0.1}; 
Sphere(15) = {x+0.366597049713857, y+0.37328012356145224, z+0.6572137829291811, 0.1}; 
Sphere(16) = {x+0.32272301761153405, y+0.3365091618177314, z+0.34720936098729094, 0.1}; 
Sphere(17) = {x+0.4760978880041422, y+0.652155831411189, z+0.6841608274695783, 0.1}; 
Sphere(18) = {x+0.6980169984560565, y+0.6917344610288069, z+0.3049821153683024, 0.1}; 
Sphere(19) = {x+0.324388552817356, y+0.6306093583852027, z+0.31264029145767136, 0.1}; 

// We first fragment all the volumes, which will leave parts of spheres
// protruding outside the cube:
v() = BooleanFragments { Volume{1}; Delete; }{ Volume{2:19}; Delete; };

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

Physical Volume(1) = {21};
Physical Volume(2) = {10,11,12,13,14,15,16,17,18,19,20,22,23,24,25,26,27,28};

