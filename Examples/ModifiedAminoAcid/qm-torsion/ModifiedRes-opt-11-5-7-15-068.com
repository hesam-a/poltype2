%RWF=/scratch/bdw2292/Gau-ModifiedRes/,100GB
%Nosave
%Chk=ModifiedRes-opt-11-5-7-15-068.chk
%Mem=20GB
%Nproc=6
#P opt=(,maxcycle=400) HF/6-31G* MaxDisk=100GB

ModifiedRes Rotatable Bond Optimization on g2-node38.bme.utexas.edu

0 1
 C    1.912592   -1.912885    0.518547
 O    2.557241   -1.974848   -0.526851
 N    0.948871   -0.974284    0.755148
 H    0.544796   -0.961124    1.687068
 C    0.613681    0.127542   -0.166815
 H    0.739619   -0.280084   -1.180259
 C    1.581864    1.323036   -0.009636
 O    2.186432    1.752054   -0.989113
 H   -0.962064    1.059646    1.022976
 H   -1.078708    1.332627   -0.719971
 C   -0.838796    0.589554    0.045527
 S   -2.027150   -0.816811   -0.108081
 C   -3.478488    0.068278   -0.145337
 N   -4.500396    0.667220   -0.172080
 N    1.714731    1.856342    1.237669
 H    2.064452   -2.619963    1.349974
 H    1.265188    1.467673    2.057281
 H    2.355932    2.634129    1.323152

11 5 7 15 F
3 5 7 15 F
3 5 7 8 F
11 5 7 8 F
3 5 11 12 F
7 5 11 12 F
5 11 12 13 F

