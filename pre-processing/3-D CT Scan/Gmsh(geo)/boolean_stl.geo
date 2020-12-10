Merge "pygalmesh_solid.stl";
Surface Loop(1) = {1};
//+
Volume(1) = {1};

eps = 1e-7;

w_max = General.MaxX + eps;
h_max = General.MaxY + eps;
l_max = General.MaxZ + eps;
w_min = General.MinX - eps;
h_min = General.MinY - eps;
l_min = General.MinZ - eps;

w = w_max - w_min;
h = h_max - h_min;
l = l_max - l_min;

//SetFactory("OpenCASCADE");
//Box(3) = {w_min, h_min, l_min, w_max, h_max, l_max};
//------------------------------------------------------------------------------------------
Point(1) = {w_max, h_min, l_min};
Point(2) = {w_max, h_max, l_min};
Point(3) = {w_min, h_max, l_min};
Point(4) = {w_min, h_min, l_max};
Point(5) = {w_max, h_min, l_max};
Point(6) = {w_max, h_max, l_max};
Point(7) = {w_min, h_max, l_max};
Point(8) = {w_min, h_min, l_min};
Line(1) = {7, 6};
Line(2) = {6, 5};
Line(3) = {5, 1};
Line(4) = {1, 8};
Line(5) = {8, 3};
Line(6) = {3, 7};
Line(7) = {7, 4};
Line(8) = {4, 8};
Line(9) = {4, 5};
Line(10) = {2, 1};
Line(11) = {2, 6};
Line(12) = {2, 3};
Line Loop(1) = {6, 1, -11, 12};
Plane Surface(10) = {1};
Line Loop(2) = {11, 2, 3, -10};
Plane Surface(20) = {2};
Line Loop(3) = {2, -9, -7, 1};
Plane Surface(30) = {-3};
Line Loop(4) = {6, 7, 8, 5};
Plane Surface(40) = {-4};
Line Loop(5) = {8, -4, -3, -9};
Plane Surface(50) = {5};
Line Loop(6) = {10, 4, 5, -12};
Plane Surface(60) = {6};
Surface Loop(3) = {60, 20, 10, 40, 30, 50, -1};
Volume(2) = {3};
//---------------------------------------------------------------------------------------------------
//---------------------------------------------------------------------------------------------------
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
//---------------------------------------------------------------------------------------------------
//---------------------------------------------------------------------------------------------------
//Mesh.CharacteristicLengthMin = 0.3;
//Mesh.CharacteristicLengthMax = 0.3;
Physical Volume(1) = {1}; 
Physical Volume(2) = {2};
