%RWF=/scratch/bdw2292/Gau-ModifiedRes/,100GB
%Nosave
%Chk=ModifiedRes-opt-3-5-11-12-192.chk
%Mem=20GB
%Nproc=6
#P opt=(,maxcycle=400) HF/6-31G* MaxDisk=100GB

ModifiedRes Rotatable Bond Optimization on g2-node38.bme.utexas.edu

0 1
 C    1.930818   -1.822209    0.498882
 O    2.632847   -1.782304   -0.518400
 N    0.946632   -0.912492    0.755099
 H    0.554589   -0.884677    1.691715
 C    0.593837    0.164262   -0.184979
 H    0.707567   -0.249620   -1.198231
 C    1.577261    1.341752   -0.022562
 O    1.209315    2.344177    0.590168
 H   -1.539187   -0.247845    0.100661
 H   -0.932758    1.170673    0.964653
 C   -0.862823    0.605808    0.030303
 S   -1.411870    1.691088   -1.355515
 C   -2.873341    2.255381   -0.696128
 N   -3.897008    2.661588   -0.257071
 N    2.804635    1.178071   -0.581395
 H    2.065256   -2.581230    1.285772
 H    3.054316    0.273587   -0.973859
 H    3.476015    1.929892   -0.500115

3 5 11 12 F
7 5 11 12 F
11 5 7 15 F
3 5 7 15 F
3 5 7 8 F
11 5 7 8 F
5 11 12 13 F
