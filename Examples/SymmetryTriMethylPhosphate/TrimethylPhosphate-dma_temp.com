%RWF=/scratch/bdw2292/Gau-TrimethylPhosphate/,100GB
%Nosave
%Chk=TrimethylPhosphate-dma_temp.chk
%Mem=20GB
%Nproc=4
#P MP2/6-311G** Sp Density=MP2 MaxDisk=100GB

TrimethylPhosphate Gaussian SP Calculation on node37.bme.utexas.edu

0 1
 P    0.092302   -0.065785   -0.361851
 O    1.274480    0.709369    0.383327
 O   -0.521204   -0.915389    0.861603
 O   -0.958255    1.106600   -0.621528
 O    0.439661   -0.841216   -1.557743
 C    2.467035   -0.021856    0.686887
 C   -1.559396   -1.850055    0.551405
 C   -1.334464    1.980489    0.446640
 H    2.923861   -0.396942   -0.232389
 H    2.243479   -0.855519    1.360431
 H    3.138626    0.680150    1.182435
 H   -2.406882   -1.342242    0.077155
 H   -1.878906   -2.282481    1.500566
 H   -1.183823   -2.631283   -0.114255
 H   -1.655559    1.407277    1.322363
 H   -2.163932    2.581030    0.072178
 H   -0.496045    2.626839    0.718866

$nbo bndidx $end

