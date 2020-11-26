SetFactory("OpenCASCADE");
Mesh.CharacteristicLengthMin = 0.07;
Mesh.CharacteristicLengthMax = 0.07;
// We start with a cube and some spheres:
Box(1) = {0, 0, 0, 1, 1, 1};
x = 0; y = 0; z = 0;

Sphere(2) = {x+0.1, y+0.1, z+0.25, 0.05}; 
Dilate {{ x+0.1, y+0.1, z+0.25},{1,1,4}} {Volume{2}; } 
Sphere(3) = {x+0.1, y+0.3, z+0.25, 0.05}; 
Dilate {{ x+0.1, y+0.3, z+0.25},{1,1,4}} {Volume{3}; } 
Sphere(4) = {x+0.1, y+0.5, z+0.25, 0.05}; 
Dilate {{ x+0.1, y+0.5, z+0.25},{1,1,4}} {Volume{4}; } 
Sphere(5) = {x+0.1, y+0.7, z+0.25, 0.05}; 
Dilate {{ x+0.1, y+0.7, z+0.25},{1,1,4}} {Volume{5}; } 
Sphere(6) = {x+0.1, y+0.9, z+0.25, 0.05}; 
Dilate {{ x+0.1, y+0.9, z+0.25},{1,1,4}} {Volume{6}; } 
Sphere(7) = {x+0.3, y+0.1, z+0.25, 0.05}; 
Dilate {{ x+0.3, y+0.1, z+0.25},{1,1,4}} {Volume{7}; } 
Sphere(8) = {x+0.3, y+0.3, z+0.25, 0.05}; 
Dilate {{ x+0.3, y+0.3, z+0.25},{1,1,4}} {Volume{8}; } 
Sphere(9) = {x+0.3, y+0.5, z+0.25, 0.05}; 
Dilate {{ x+0.3, y+0.5, z+0.25},{1,1,4}} {Volume{9}; } 
Sphere(10) = {x+0.3, y+0.7, z+0.25, 0.05}; 
Dilate {{ x+0.3, y+0.7, z+0.25},{1,1,4}} {Volume{10}; } 
Sphere(11) = {x+0.3, y+0.9, z+0.25, 0.05}; 
Dilate {{ x+0.3, y+0.9, z+0.25},{1,1,4}} {Volume{11}; } 
Sphere(12) = {x+0.5, y+0.1, z+0.25, 0.05}; 
Dilate {{ x+0.5, y+0.1, z+0.25},{1,1,4}} {Volume{12}; } 
Sphere(13) = {x+0.5, y+0.3, z+0.25, 0.05}; 
Dilate {{ x+0.5, y+0.3, z+0.25},{1,1,4}} {Volume{13}; } 
Sphere(14) = {x+0.5, y+0.5, z+0.25, 0.05}; 
Dilate {{ x+0.5, y+0.5, z+0.25},{1,1,4}} {Volume{14}; } 
Sphere(15) = {x+0.5, y+0.7, z+0.25, 0.05}; 
Dilate {{ x+0.5, y+0.7, z+0.25},{1,1,4}} {Volume{15}; } 
Sphere(16) = {x+0.5, y+0.9, z+0.25, 0.05}; 
Dilate {{ x+0.5, y+0.9, z+0.25},{1,1,4}} {Volume{16}; } 
Sphere(17) = {x+0.7, y+0.1, z+0.25, 0.05}; 
Dilate {{ x+0.7, y+0.1, z+0.25},{1,1,4}} {Volume{17}; } 
Sphere(18) = {x+0.7, y+0.3, z+0.25, 0.05}; 
Dilate {{ x+0.7, y+0.3, z+0.25},{1,1,4}} {Volume{18}; } 
Sphere(19) = {x+0.7, y+0.5, z+0.25, 0.05}; 
Dilate {{ x+0.7, y+0.5, z+0.25},{1,1,4}} {Volume{19}; } 
Sphere(20) = {x+0.7, y+0.7, z+0.25, 0.05}; 
Dilate {{ x+0.7, y+0.7, z+0.25},{1,1,4}} {Volume{20}; } 
Sphere(21) = {x+0.7, y+0.9, z+0.25, 0.05}; 
Dilate {{ x+0.7, y+0.9, z+0.25},{1,1,4}} {Volume{21}; } 
Sphere(22) = {x+0.9, y+0.1, z+0.25, 0.05}; 
Dilate {{ x+0.9, y+0.1, z+0.25},{1,1,4}} {Volume{22}; } 
Sphere(23) = {x+0.9, y+0.3, z+0.25, 0.05}; 
Dilate {{ x+0.9, y+0.3, z+0.25},{1,1,4}} {Volume{23}; } 
Sphere(24) = {x+0.9, y+0.5, z+0.25, 0.05}; 
Dilate {{ x+0.9, y+0.5, z+0.25},{1,1,4}} {Volume{24}; } 
Sphere(25) = {x+0.9, y+0.7, z+0.25, 0.05}; 
Dilate {{ x+0.9, y+0.7, z+0.25},{1,1,4}} {Volume{25}; } 
Sphere(26) = {x+0.9, y+0.9, z+0.25, 0.05}; 
Dilate {{ x+0.9, y+0.9, z+0.25},{1,1,4}} {Volume{26}; } 
Sphere(27) = {x+0.1, y+0.1, z+0.75, 0.05}; 
Dilate {{ x+0.1, y+0.1, z+0.75},{1,1,4}} {Volume{27}; } 
Sphere(28) = {x+0.1, y+0.3, z+0.75, 0.05}; 
Dilate {{ x+0.1, y+0.3, z+0.75},{1,1,4}} {Volume{28}; } 
Sphere(29) = {x+0.1, y+0.5, z+0.75, 0.05}; 
Dilate {{ x+0.1, y+0.5, z+0.75},{1,1,4}} {Volume{29}; } 
Sphere(30) = {x+0.1, y+0.7, z+0.75, 0.05}; 
Dilate {{ x+0.1, y+0.7, z+0.75},{1,1,4}} {Volume{30}; } 
Sphere(31) = {x+0.1, y+0.9, z+0.75, 0.05}; 
Dilate {{ x+0.1, y+0.9, z+0.75},{1,1,4}} {Volume{31}; } 
Sphere(32) = {x+0.3, y+0.1, z+0.75, 0.05}; 
Dilate {{ x+0.3, y+0.1, z+0.75},{1,1,4}} {Volume{32}; } 
Sphere(33) = {x+0.3, y+0.3, z+0.75, 0.05}; 
Dilate {{ x+0.3, y+0.3, z+0.75},{1,1,4}} {Volume{33}; } 
Sphere(34) = {x+0.3, y+0.5, z+0.75, 0.05}; 
Dilate {{ x+0.3, y+0.5, z+0.75},{1,1,4}} {Volume{34}; } 
Sphere(35) = {x+0.3, y+0.7, z+0.75, 0.05}; 
Dilate {{ x+0.3, y+0.7, z+0.75},{1,1,4}} {Volume{35}; } 
Sphere(36) = {x+0.3, y+0.9, z+0.75, 0.05}; 
Dilate {{ x+0.3, y+0.9, z+0.75},{1,1,4}} {Volume{36}; } 
Sphere(37) = {x+0.5, y+0.1, z+0.75, 0.05}; 
Dilate {{ x+0.5, y+0.1, z+0.75},{1,1,4}} {Volume{37}; } 
Sphere(38) = {x+0.5, y+0.3, z+0.75, 0.05}; 
Dilate {{ x+0.5, y+0.3, z+0.75},{1,1,4}} {Volume{38}; } 
Sphere(39) = {x+0.5, y+0.5, z+0.75, 0.05}; 
Dilate {{ x+0.5, y+0.5, z+0.75},{1,1,4}} {Volume{39}; } 
Sphere(40) = {x+0.5, y+0.7, z+0.75, 0.05}; 
Dilate {{ x+0.5, y+0.7, z+0.75},{1,1,4}} {Volume{40}; } 
Sphere(41) = {x+0.5, y+0.9, z+0.75, 0.05}; 
Dilate {{ x+0.5, y+0.9, z+0.75},{1,1,4}} {Volume{41}; } 
Sphere(42) = {x+0.7, y+0.1, z+0.75, 0.05}; 
Dilate {{ x+0.7, y+0.1, z+0.75},{1,1,4}} {Volume{42}; } 
Sphere(43) = {x+0.7, y+0.3, z+0.75, 0.05}; 
Dilate {{ x+0.7, y+0.3, z+0.75},{1,1,4}} {Volume{43}; } 
Sphere(44) = {x+0.7, y+0.5, z+0.75, 0.05}; 
Dilate {{ x+0.7, y+0.5, z+0.75},{1,1,4}} {Volume{44}; } 
Sphere(45) = {x+0.7, y+0.7, z+0.75, 0.05}; 
Dilate {{ x+0.7, y+0.7, z+0.75},{1,1,4}} {Volume{45}; } 
Sphere(46) = {x+0.7, y+0.9, z+0.75, 0.05}; 
Dilate {{ x+0.7, y+0.9, z+0.75},{1,1,4}} {Volume{46}; } 
Sphere(47) = {x+0.9, y+0.1, z+0.75, 0.05}; 
Dilate {{ x+0.9, y+0.1, z+0.75},{1,1,4}} {Volume{47}; } 
Sphere(48) = {x+0.9, y+0.3, z+0.75, 0.05}; 
Dilate {{ x+0.9, y+0.3, z+0.75},{1,1,4}} {Volume{48}; } 
Sphere(49) = {x+0.9, y+0.5, z+0.75, 0.05}; 
Dilate {{ x+0.9, y+0.5, z+0.75},{1,1,4}} {Volume{49}; } 
Sphere(50) = {x+0.9, y+0.7, z+0.75, 0.05}; 
Dilate {{ x+0.9, y+0.7, z+0.75},{1,1,4}} {Volume{50}; } 
Sphere(51) = {x+0.9, y+0.9, z+0.75, 0.05}; 
Dilate {{ x+0.9, y+0.9, z+0.75},{1,1,4}} {Volume{51}; } 

// We first fragment all the volumes, which will leave parts of spheres
// protruding outside the cube:
v() = BooleanFragments { Volume{1}; Delete; }{ Volume{2:51}; Delete; };

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

Physical Volume(1) = {52};
Physical Volume(2) = {2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51};
