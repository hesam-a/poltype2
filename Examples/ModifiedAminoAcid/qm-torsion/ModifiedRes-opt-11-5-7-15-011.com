%RWF=/scratch/bdw2292/Gau-ModifiedRes/,100GB
%Nosave
%Chk=ModifiedRes-opt-11-5-7-15-011.chk
%Mem=20GB
%Nproc=6
#P opt=(,maxcycle=400) HF/6-31G* MaxDisk=100GB

ModifiedRes Rotatable Bond Optimization on g2-node38.bme.utexas.edu

0 1
 C    1.894151   -1.880909    0.515472
 O    2.431346   -2.049765   -0.579351
 N    0.929763   -0.942009    0.755031
 H    0.523233   -0.932901    1.686250
 C    0.586507    0.159502   -0.164515
 H    0.710782   -0.223075   -1.188368
 C    1.598512    1.326112    0.019290
 O    2.766993    1.168780   -0.319573
 H   -1.050595    1.017066    1.024185
 H   -1.144832    1.320690   -0.711208
 C   -0.883722    0.572118    0.041541
 S   -2.023655   -0.870044   -0.158838
 C   -3.494169   -0.018003   -0.196749
 N   -4.505255    0.598676   -0.179226
 N    1.172973    2.505219    0.554787
 H    2.127657   -2.510532    1.389621
 H    0.217136    2.700784    0.820587
 H    1.876477    3.226691    0.645463

11 5 7 15 F
3 5 7 15 F
3 5 7 8 F
11 5 7 8 F
3 5 11 12 F
7 5 11 12 F
5 11 12 13 F
