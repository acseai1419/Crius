SetFactory("OpenCASCADE");
//Starting with a box of length = 1
Box(1) = {0, 0, 0, 1, 1, 1};
x = 0; y = 0; z = 0; 
//-----------------------------------------------------------------------------------------------------------------------
//Copy in the section below the geometric information generated from the pre-processing module in meshes/txt_mesh/
//The geometric information starts from the first line until
//this line -> v() = BooleanFragments { Volume{1}; Delete; }{ Volume{2:n}; Delete; };
//-----------------------------------------------------------------------------------------------------------------------
Sphere(2) = {x+0.16685086439745317, y+0.4846283783650761, z+0.47290641987348825, 0.14381351127913403}; 
Sphere(3) = {x+0.8027615085456123, y+0.19604786238827848, z+0.5485438192352494, 0.14142427951438402}; 
Sphere(4) = {x+0.481902205835157, y+0.39464635089509703, z+0.40731262005553076, 0.14132046810172993}; 
Sphere(5) = {x+0.5781365177720581, y+0.2979909434251735, z+0.8346386615549028, 0.14065788996604442}; 
Sphere(6) = {x+0.8122637404981911, y+0.2731910866466588, z+0.21915545364130357, 0.13971812854771667}; 
Sphere(7) = {x+0.8169971304284256, y+0.31561605917851066, z+0.748630814469306, 0.13307534216754568}; 
Sphere(8) = {x+0.481012129564619, y+0.6325851254558246, z+0.2299296179004671, 0.13283201064410372}; 
Sphere(9) = {x+0.28520683668334484, y+0.7607098129539319, z+0.5870012023486945, 0.13246774259543695}; 
Sphere(10) = {x+0.5074069797228882, y+0.7802872399951781, z+0.8035374555340449, 0.13049909615336508}; 
Sphere(11) = {x+0.4665925495418195, y+0.8544066707172495, z+0.47019194908740614, 0.12769866690728832}; 
Sphere(12) = {x+0.7304913854249264, y+0.5836666096794457, z+0.22639182380490622, 0.12697949253520174}; 
Sphere(13) = {x+0.3014309636395137, y+0.2085405198144325, z+0.7010969695526791, 0.12683063535444503}; 
Sphere(14) = {x+0.1895397485544013, y+0.16501648186706114, z+0.36046935319626106, 0.1262562573662967}; 
Sphere(15) = {x+0.13051962618836752, y+0.6939536780954029, z+0.37276267524587003, 0.12551214530209354}; 
Sphere(16) = {x+0.8281445888950063, y+0.7619514330752639, z+0.16083506227062017, 0.12464347670286258}; 
Sphere(17) = {x+0.2304108689626337, y+0.32665231647368465, z+0.14707067451992495, 0.12394612556822604}; 
Sphere(18) = {x+0.8447274887397419, y+0.8048270634936358, z+0.5929762121595431, 0.12150174797947906}; 
Sphere(19) = {x+0.24225893630633943, y+0.6803559651830454, z+0.828752947563, 0.11953991817892683}; 
Sphere(20) = {x+0.7152341143208074, y+0.5402803567400571, z+0.5209491945375624, 0.11809940548327806}; 
Sphere(21) = {x+0.5188338775506187, y+0.6237201977539991, z+0.5927558415650785, 0.11747248662306263}; 
Sphere(22) = {x+0.7795735758471233, y+0.8691363295030232, z+0.7896597762750909, 0.11640685164313479}; 
Sphere(23) = {x+0.19415157281994788, y+0.4006294635583018, z+0.7660793331245752, 0.11408674981760968}; 
Sphere(24) = {x+0.808982208910763, y+0.7145903120231443, z+0.36789944679536957, 0.1137324388396041}; 
Sphere(25) = {x+0.8333210661079145, y+0.11345777824082512, z+0.8072368184824135, 0.1086557340643371}; 
Sphere(26) = {x+0.28370486481787155, y+0.6222650760575793, z+0.142936868365783, 0.10784215253628218}; 
Sphere(27) = {x+0.5843851918484442, y+0.2310217966442596, z+0.2777364232067207, 0.10601719835696279}; 
Sphere(28) = {x+0.4909249130993133, y+0.4304736079958264, z+0.16686546355628637, 0.10506901791572315}; 
Sphere(29) = {x+0.43641793716977206, y+0.859572887251586, z+0.2727587630167976, 0.10491456330579957}; 
Sphere(30) = {x+0.7337185080638418, y+0.6651841195576315, z+0.8065460905929416, 0.1041176715287523}; 
Sphere(31) = {x+0.6048732318751068, y+0.2515039354636426, z+0.4930513854035007, 0.10349871072239533}; 
Sphere(32) = {x+0.6367966803960967, y+0.7541145978044542, z+0.4842580707246974, 0.10071172602682896}; 
v() = BooleanFragments { Volume{1}; Delete; }{ Volume{2 :32}; Delete; };
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
Physical Volume(1) = {20}; 
Physical Volume(2) = {10, 14, 17, 19, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72};
Mesh.CharacteristicLengthMin = 0.07; 
Mesh.CharacteristicLengthMax = 0.07;
//------------------------------------------------------------------------------------------------------------------------------------------
