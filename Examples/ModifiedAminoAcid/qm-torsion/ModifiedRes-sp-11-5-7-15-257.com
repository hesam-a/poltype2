%RWF=/scratch/bdw2292/Gau-ModifiedRes/,100GB
%Nosave
%Chk=ModifiedRes-sp-11-5-7-15-257.chk
%Mem=20GB
%Nproc=6
#P MP2/6-311++G** SP SCF=(qc,maxcycle=800) Guess=Indo MaxDisk=100GB Pop=NBORead

ModifiedRes Rotatable Bond SP Calculation on g2-node38.bme.utexas.edu

0 1
 C    1.890235   -2.004980    0.804690
 O    2.558863   -2.127521   -0.224906
 N    0.961773   -1.018874    0.965020
 H    0.498022   -0.936952    1.865174
 C    0.726244    0.024191   -0.050146
 H    0.914907   -0.446586   -1.026202
 C    1.717197    1.187931    0.147834
 O    1.897264    1.629501    1.282725
 H   -0.911254    1.026583    0.976471
 H   -0.855571    1.305150   -0.776338
 C   -0.714861    0.558118    0.008143
 S   -1.933956   -0.802819   -0.265852
 C   -3.353623    0.128990   -0.362351
 N   -4.333792    0.794411   -0.393484
 N    2.334113    1.657975   -0.969221
 H    1.992337   -2.682558    1.667057
 H    2.265749    1.158128   -1.846999
 H    2.995654    2.413584   -0.849276

