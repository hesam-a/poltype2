%RWF=/scratch/bdw2292/Gau-ModifiedRes/,100GB
%Nosave
%Chk=ModifiedRes-opt-11-5-7-15-257.chk
%Mem=20GB
%Nproc=6
#P opt=(,maxcycle=400) HF/6-31G* MaxDisk=100GB

ModifiedRes Rotatable Bond Optimization on g2-node38.bme.utexas.edu

0 1
 C    1.954709   -1.825555    0.480872
 O    2.555215   -1.847945   -0.596579
 N    0.964299   -0.927224    0.749924
 H    0.585024   -0.900952    1.691989
 C    0.589392    0.143321   -0.193340
 H    0.701141   -0.283933   -1.200869
 C    1.555949    1.332111   -0.026470
 O    1.822312    1.727561    1.108531
 H   -0.964347    1.080160    0.994299
 H   -1.124271    1.327019   -0.755834
 C   -0.864027    0.600050    0.016779
 S   -2.039611   -0.820456   -0.099556
 C   -3.504587    0.042627   -0.132649
 N   -4.536887    0.624204   -0.157561
 N    2.054234    1.874677   -1.169153
 H    2.172994   -2.527079    1.301407
 H    1.940928    1.401614   -2.057029
 H    2.694533    2.651301   -1.070262

11 5 7 15 F
3 5 7 15 F
3 5 7 8 F
11 5 7 8 F
3 5 11 12 F
7 5 11 12 F
5 11 12 13 F

