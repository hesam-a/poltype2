%RWF=/scratch/bdw2292/Gau-ModifiedRes/,100GB
%Nosave
%Chk=ModifiedRes-sp-11-5-7-15-049.chk
%Mem=20GB
%Nproc=6
#P MP2/6-311++G** SP SCF=(qc,maxcycle=800) Guess=Indo MaxDisk=100GB Pop=NBORead

ModifiedRes Rotatable Bond SP Calculation on g2-node38.bme.utexas.edu

0 1
 C    1.852586   -2.168796   -0.220528
 O    2.158740   -2.287227   -1.406077
 N    1.131223   -1.126010    0.299927
 H    0.981909   -1.123393    1.303546
 C    0.707773    0.056701   -0.485710
 H    0.531786   -0.297143   -1.514747
 C    1.841334    1.114588   -0.510853
 O    2.496581    1.282549   -1.531158
 H   -0.497394    1.040573    1.124300
 H   -0.920001    1.525218   -0.524405
 C   -0.600694    0.671385    0.090154
 S   -1.867397   -0.691987    0.021003
 C   -3.328492    0.067985    0.428727
 N   -4.345983    0.597221    0.712662
 N    2.073453    1.834837    0.616463
 H    2.118239   -2.926034    0.526982
 H    1.565843    1.715697    1.482772
 H    2.750387    2.578458    0.538549
