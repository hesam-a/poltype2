%RWF=/scratch/bdw2292/Gau-ModifiedRes/,100GB
%Nosave
%Chk=ModifiedRes-sp-11-5-7-15-106.chk
%Mem=20GB
%Nproc=6
#P MP2/6-311++G** SP SCF=(qc,maxcycle=800) Guess=Indo MaxDisk=100GB Pop=NBORead

ModifiedRes Rotatable Bond SP Calculation on g2-node38.bme.utexas.edu

0 1
 C    1.962982   -1.959193    0.006038
 O    2.395800   -2.037143   -1.142710
 N    1.096432   -0.985434    0.413380
 H    0.871606   -0.946378    1.403909
 C    0.598469    0.097402   -0.458092
 H    0.538227   -0.327826   -1.469647
 C    1.577026    1.299614   -0.485745
 O    1.451807    2.123502   -1.391063
 H   -0.724233    1.010282    1.012411
 H   -1.132319    1.360588   -0.681605
 C   -0.781256    0.586292    0.007077
 S   -2.009281   -0.793912    0.006285
 C   -3.420525    0.098168    0.329748
 N   -4.417103    0.698403    0.555561
 N    2.530030    1.413150    0.481413
 H    2.247707   -2.671127    0.797407
 H    2.714191    0.687851    1.161931
 H    3.149978    2.209246    0.407049
