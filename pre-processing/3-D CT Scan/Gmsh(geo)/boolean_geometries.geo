SetFactory("OpenCASCADE");
//v() = ShapeFromFile("meshfix_inside.brep");
Merge "meshfix_inside.brep";
Geometry.OCCBoundsUseStl = 1;
bbox() = BoundingBox Volume{1};
w_min = bbox(0);
h_min = bbox(1);
l_min = bbox(2);
w_max = bbox(3);
h_max = bbox(4);
l_max = bbox(5);
Box(2) = {w_min,h_min,l_min,w_max,h_max,l_max};
v() = BooleanFragments { Volume{2}; Delete; }{ Volume{1}; Delete; };
Geometry.OCCBoundsUseStl = 1;
eps = 1e-3;

// First we get all surfaces on the left:
Sxmin() = Surface In BoundingBox{w_min-eps, h_min-eps, l_min-eps, w_min+eps, h_max+eps, l_max+eps};

For i In {0:#Sxmin()-w}
  // Then we get the bounding box of each left surface
  bb() = BoundingBox Surface { Sxmin(i) };
  // We translate the bounding box to the right and look for surfaces inside i
  Sxmax() = Surface In BoundingBox { bb(0)-eps+w, bb(1)-eps, bb(2)-eps,
                                     bb(3)+eps+w, bb(4)+eps, bb(5)+eps };
  // For all the matches, we compare the corresponding bounding boxes...
  For j In {0:#Sxmax()-w}
    bb2() = BoundingBox Surface { Sxmax(j) };
    bb2(0) -= w;
    bb2(3) -= w;
    // ...and if they match, we apply the periodicity constraint
    If(Fabs(bb2(0)-bb(0)) < eps && Fabs(bb2(1)-bb(1)) < eps &&
       Fabs(bb2(2)-bb(2)) < eps && Fabs(bb2(3)-bb(3)) < eps &&
       Fabs(bb2(4)-bb(4)) < eps && Fabs(bb2(5)-bb(5)) < eps)
      Periodic Surface {Sxmax(j)} = {Sxmin(i)} Translate {w,0,0};
    EndIf
  EndFor
EndFor

// Then we get all surfaces on the outter:
Symin() = Surface In BoundingBox{w_min-eps, h_min-eps, l_min-eps, w_max+eps, h_min+eps, l_max+eps};

For i In {0:#Symin()-h}
  // Then we get the bounding box of each outter surface
  bb() = BoundingBox Surface { Symin(i) };
  // We translate the bounding box to the right and look for surfaces inside i
  Symax() = Surface In BoundingBox { bb(0)-eps, bb(1)-eps+h, bb(2)-eps,
                                     bb(3)+eps, bb(4)+eps+h, bb(5)+eps };
  // For all the matches, we compare the corresponding bounding boxes...
  For j In {0:#Symax()-h}
    bb2() = BoundingBox Surface { Symax(j) };
    bb2(1) -= h;
    bb2(4) -= h;
    // ...and if they match, we apply the periodicity constraint
    If(Fabs(bb2(0)-bb(0)) < eps && Fabs(bb2(1)-bb(1)) < eps &&
       Fabs(bb2(2)-bb(2)) < eps && Fabs(bb2(3)-bb(3)) < eps &&
       Fabs(bb2(4)-bb(4)) < eps && Fabs(bb2(5)-bb(5)) < eps)
      Periodic Surface {Symax(j)} = {Symin(i)} Translate {0,h,0};
    EndIf
  EndFor
EndFor

// Then we get all surfaces on the bottom:
Szmin() = Surface In BoundingBox{w_min-eps, h_min-eps, l_min-eps, w_max+eps, h_max+eps, l_min+eps};

For i In {0:#Szmin()-l}
  // Then we get the bounding box of each left surface
  bb() = BoundingBox Surface { Szmin(i) };
  // We translate the bounding box to the right and look for surfaces inside i
  Szmax() = Surface In BoundingBox { bb(0)-eps, bb(1)-eps, bb(2)-eps+l,
                                     bb(3)+eps, bb(4)+eps, bb(5)+eps+l };
  // For all the matches, we compare the corresponding bounding boxes...
  For j In {0:#Szmax()-l}
    bb2() = BoundingBox Surface { Szmax(j) };
    bb2(2) -= l;
    bb2(5) -= l;
    // ...and if they match, we apply the periodicity constraint
    If(Fabs(bb2(0)-bb(0)) < eps && Fabs(bb2(1)-bb(1)) < eps &&
       Fabs(bb2(2)-bb(2)) < eps && Fabs(bb2(3)-bb(3)) < eps &&
       Fabs(bb2(4)-bb(4)) < eps && Fabs(bb2(5)-bb(5)) < eps)
      Periodic Surface {Szmax(j)} = {Szmin(i)} Translate {0,0,l};
    EndIf
  EndFor
EndFor

Physical Volume(1) = {1}; 
Physical Volume(2) = {2};
