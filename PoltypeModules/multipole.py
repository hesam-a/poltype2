import electrostaticpotential as esp
import time
import os
import sys
import openbabel
import shutil
import re
from collections import deque



def AddPolarizeCommentsToKey(poltype,keyfilename,polartypetotransferinfo):
    temp=open(keyfilename,'r')
    results=temp.readlines()
    temp.close()
    tempname=keyfilename.replace('.key','_temp.key')
    temp=open(tempname,'w')
    for line in results:
        if 'polarize' in line and '#' not in line:
            linesplit=line.split()
            typenum=linesplit[1]
            comments=polartypetotransferinfo[typenum]
            line=comments+line
        temp.write(line)
    temp.close()
    os.remove(keyfilename)
    os.rename(tempname,keyfilename)



def SanitizeMultipoleFrames(poltype,keyfilename): # pearl script for averging only understands 0 and not empty spaces for parsing
    temp=open(keyfilename,'r')
    results=temp.readlines()
    temp.close()
    tempname=keyfilename.replace('.key','_temp.key')
    temp=open(tempname,'w')
    extraspace='     '
    for line in results:
        if 'multipole' in line:
            linesplit=line.split()
            realsplit=re.split(r'(\s+)', line)
            if len(linesplit)==3:
                realsplit=realsplit[:3]+[extraspace]+['0']+[extraspace]+['0']+realsplit[3:]
            elif len(linesplit)==4:
                realsplit=realsplit[:5]+[extraspace]+['0']+realsplit[5:]
            line=''.join(realsplit)
        temp.write(line)
    temp.close()
    os.remove(keyfilename)
    os.rename(tempname,keyfilename)

def CheckIfAllAtomsSameClass(poltype,classlist):
    allsymm=True
    if len(classlist)>=1:
        firstsymm=poltype.idxtosymclass[classlist[0].GetIdx()]
        for atom in classlist:
            atomidx=atom.GetIdx()
            symmetry=poltype.idxtosymclass[atomidx]
            if symmetry!=firstsymm:
                allsymm=False
    return allsymm

def RemoveFromList(poltype,atomlist,atm):
    newatmlist=[]
    idx=atm.GetIdx()
    for newatm in atomlist:
        if idx!=newatm.GetIdx():
            newatmlist.append(newatm)
    return newatmlist


def AtLeastOneHeavyLf1NeighbNotAtom(poltype,lf1atom,atom):
    foundatleastoneheavy=False
    checkneighbs=[neighb for neighb in openbabel.OBAtomAtomIter(lf1atom)]
    for neighb in checkneighbs:
        if neighb.GetIdx()!=atom.GetIdx() and neighb.GetAtomicNum()!=1:
            foundatleastoneheavy=True
    return foundatleastoneheavy


def AtLeastOneHeavyNeighb(poltype,atom):
    foundatleastoneheavy=False
    checkneighbs=[neighb for neighb in openbabel.OBAtomAtomIter(atom)]
    for neighb in checkneighbs:
        if neighb.GetAtomicNum()!=1:
            foundatleastoneheavy=True
    return foundatleastoneheavy


def GrabHeavyAtomIdx(poltype,lf1atom,atom):
    checkneighbs=[neighb for neighb in openbabel.OBAtomAtomIter(lf1atom)]
    for neighb in checkneighbs:
        if neighb.GetIdx()!=atom.GetIdx() and neighb.GetAtomicNum()!=1:
            return neighb.GetIdx()

def FindUniqueNonRepeatingNeighbors(poltype,nlist):
    d={}
    for b in nlist:
        typenum= poltype.idxtosymclass[b.GetIdx()]
        if typenum not in d.keys():
            d[typenum]=0
        d[typenum]+=1
    uniquetypeneighbsnorepeat=[]
    for typenum in d.keys():
        repeat=d[typenum]
        if repeat==1:
            idx=GrabIndexFromUniqueTypeNumber(poltype,nlist,typenum)
            uniquetypeneighbsnorepeat.append(idx)
    sorteduniquetypeneighbsnorepeat=sorted(uniquetypeneighbsnorepeat,reverse=True)
    return sorteduniquetypeneighbsnorepeat

def GrabIndexFromUniqueTypeNumber(poltype,nlist,typenum):
    for b in nlist:
        idx=b.GetIdx()
        typenumber= poltype.idxtosymclass[idx]
        if typenumber==typenum:
            return idx

def GrabIndexesFromUniqueTypeNumber(poltype,nlist,typenum):
    idxlist=[]
    for b in nlist:
        idx=b.GetIdx()
        typenumber= poltype.idxtosymclass[idx]
        if typenumber==typenum:
            if idx not in idxlist:
                idxlist.append(idx)
    return idxlist




def CheckIfNeighbHasSameType(poltype,a,neighbs):
    check=False
    reftype=poltype.idxtosymclass[a.GetIdx()]
    neighbtypes=[poltype.idxtosymclass[b.GetIdx()] for b in neighbs]
    if reftype in neighbtypes:
        check=True
    return check

def GrabNumberOfConnectedHydrogens(poltype,highestsymneighbnorepeat):
    atomneighbs=[neighb for neighb in openbabel.OBAtomAtomIter(highestsymneighbnorepeat)]
    hydnum=0
    for atom in atomneighbs:
        if atom.GetAtomicNum()==1:
            hydnum+=1
    return hydnum

   
def gen_peditinfile(poltype,mol,polarindextopolarizeprm):
    lfzerox = [ False ] * mol.NumAtoms()
    atomindextoremovedipquad={} # for methane need to make dipole and quadupole on the carbon zeroed out, will return this for post proccesing the keyfile after poledit is run
    atomindextoremovedipquadcross={}
    atomtypetospecialtrace={} # for H on CH4 need to make sure Qxx=Qyy=-1/2*Qzz
    idxtobisecthenzbool={}
    idxtobisectidxs={}
    idxtotrisecbool={}
    idxtotrisectidxs={}
    # Assign local frame for atom a based on the symmetry classes of the atoms it is bound to
    atomiter=openbabel.OBMolAtomIter(mol)
    poltype.localframe2 = list(poltype.localframe2)
    for a in atomiter:
        idxtobisecthenzbool[a.GetIdx()]=False
        idxtotrisecbool[a.GetIdx()]=False
    for atom in openbabel.OBMolAtomIter(mol):
        atomidx=atom.GetIdx()
        val=atom.GetValence()
        atomicnum=atom.GetAtomicNum()
        atomneighbs=[neighb for neighb in openbabel.OBAtomAtomIter(atom)]
        uniqueneighbtypes=list(set([poltype.idxtosymclass[b.GetIdx()] for b in atomneighbs]))
        sorteduniquetypeneighbsnorepeat=FindUniqueNonRepeatingNeighbors(poltype,atomneighbs)
        foundcase=False
        numhyds=GrabNumberOfConnectedHydrogens(poltype,atom)
        if len(sorteduniquetypeneighbsnorepeat)!=0:
            highestsymneighbnorepeatidx=sorteduniquetypeneighbsnorepeat[0]
            highestsymneighbnorepeat=mol.GetAtom(highestsymneighbnorepeatidx)
            numhydsneighb=GrabNumberOfConnectedHydrogens(poltype,highestsymneighbnorepeat)
            highestsymneighbnorepeatval=highestsymneighbnorepeat.GetValence()
            neighbsofneighb=[neighb for neighb in openbabel.OBAtomAtomIter(highestsymneighbnorepeat)]
            uniqueneighbtypesofhighestsymneighbnorepeat=list(set([poltype.idxtosymclass[b.GetIdx()] for b in neighbsofneighb]))
            neighbsofneighbwithoutatom=RemoveFromList(poltype,neighbsofneighb,atom)
            neighbswithoutatom=RemoveFromList(poltype,atomneighbs,atom)
            uniqueneighbtypesofhighestsymneighbnorepeatwithoutatom=list(set([poltype.idxtosymclass[b.GetIdx()] for b in neighbsofneighbwithoutatom]))
            if highestsymneighbnorepeatval==3 and CheckIfAllAtomsSameClass(poltype,[neighb for neighb in openbabel.OBAtomAtomIter(highestsymneighbnorepeat)]): # then this is like the H on Ammonia and we can use z-then bisector
                poltype.localframe1[atomidx-1]=sorteduniquetypeneighbsnorepeat[0]
                idxtobisecthenzbool[atomidx]=True
                bisectidxs=[atm.GetIdx() for atm in neighbsofneighbwithoutatom]
                idxtobisectidxs[atomidx]=bisectidxs
                foundcase=True
            elif ((len(uniqueneighbtypes)==2 and val==4)) and val==highestsymneighbnorepeatval and len(uniqueneighbtypesofhighestsymneighbnorepeat)==2: # then this is like CH3PO3, we want z-onlytrisector would also work
                poltype.localframe1[atomidx-1]=sorteduniquetypeneighbsnorepeat[0]
                poltype.localframe2[atomidx - 1] = 0
                lfzerox[atomidx - 1]=True
                foundcase=True
                
            elif ((val==4 and len(uniqueneighbtypes)==2 and highestsymneighbnorepeatval==3) or (val==3 and len(uniqueneighbtypes)==2 and (highestsymneighbnorepeatval==3 or highestsymneighbnorepeatval==4))) and len(uniqueneighbtypesofhighestsymneighbnorepeat)==2 and len(uniqueneighbtypesofhighestsymneighbnorepeatwithoutatom)==1:  # then this is like methyl-amine and we can use the two atoms with same symmetry class to do a z-then-bisector, need len(uniqueneighbtypesofhighestsymneighbnorepeatwithoutatom)==1 otherwise hits dimethylamine. Need to specify numhyds otherwise will hit nitrobenzene N/C

                if numhyds==2 or numhydsneighb==2:
                    idxtobisecthenzbool[atomidx]=True
                    if atomicnum==6:
                        bisectidxs=[atm.GetIdx() for atm in neighbsofneighbwithoutatom]
                    else:
                        neighbswithoutatom=RemoveFromList(poltype,atomneighbs,highestsymneighbnorepeat)
                        bisectidxs=[atm.GetIdx() for atm in neighbswithoutatom]
                       
                    idxtobisectidxs[atomidx]=bisectidxs
                    poltype.localframe1[atomidx - 1] = highestsymneighbnorepeatidx
                    foundcase=True
                else:
                    foundcase=True
                    poltype.localframe1[atomidx-1]=sorteduniquetypeneighbsnorepeat[0]
                    poltype.localframe2[atomidx - 1] = 0
                    lfzerox[atomidx - 1]=True

                # now make sure neighboring atom (lf1) also is using z-then-bisector
            elif ((val==1 and (highestsymneighbnorepeatval==3) and atomicnum==1) or ((val==3) and highestsymneighbnorepeatval==1)) and numhydsneighb<=1 and len(uniqueneighbtypes)<=2 and len(uniqueneighbtypesofhighestsymneighbnorepeat)<=2: #dimethylamine
                poltype.localframe1[atomidx-1]=sorteduniquetypeneighbsnorepeat[0]
                poltype.localframe2[atomidx - 1] = 0
                lfzerox[atomidx - 1]=True
                foundcase=True
            elif (((val==3) and (highestsymneighbnorepeatval==4))) and numhydsneighb<=2 and len(uniqueneighbtypes)<=2 and len(uniqueneighbtypesofhighestsymneighbnorepeat)<=3:
                poltype.localframe1[atomidx-1]=sorteduniquetypeneighbsnorepeat[0]
                poltype.localframe2[atomidx - 1] = 0
                lfzerox[atomidx - 1]=True
                foundcase=True
            elif val==4 and len(uniqueneighbtypes)==2 and highestsymneighbnorepeatval==1: # ammonium
                neighbswithoutatom=RemoveFromList(poltype,atomneighbs,highestsymneighbnorepeat)
                idxtotrisecbool[atomidx]=True
                trisectidxs=[atm.GetIdx() for atm in neighbswithoutatom]
                idxtotrisectidxs[atomidx]=trisectidxs
                lfzerox[atomidx - 1]=True 
                foundcase=True
            elif val==1 and highestsymneighbnorepeatval==4 and len(uniqueneighbtypesofhighestsymneighbnorepeat)==2: # ammonium H
                poltype.localframe1[atomidx-1]=sorteduniquetypeneighbsnorepeat[0]
                poltype.localframe2[atomidx - 1] = 0
                lfzerox[atomidx - 1]=True
                foundcase=True



        if foundcase==False:
            if val==1 and CheckIfAllAtomsSameClass(poltype,[neighb for neighb in openbabel.OBAtomAtomIter(atomneighbs[0])]) and atomneighbs[0].GetValence()==4: # then this is like H in Methane, we want Z-only
             
                poltype.localframe1[atomidx-1]=sorteduniquetypeneighbsnorepeat[0]
                poltype.localframe2[atomidx - 1] = 0
                lfzerox[atomidx - 1]=True
                zonly=True
                atomtypetospecialtrace[atomidx]=True
                atomindextoremovedipquadcross[atomidx]=True
            elif CheckIfAllAtomsSameClass(poltype,atomneighbs) and not AtLeastOneHeavyNeighb(poltype,atom) and val==4: # then this is like carbon in Methane, we want Z-only
                idxlist=GrabIndexesFromUniqueTypeNumber(poltype,atomneighbs,uniqueneighbtypes[0])
                poltype.localframe1[atomidx-1]=idxlist[0]
                poltype.localframe2[atomidx - 1] = 0
                lfzerox[atomidx - 1]=True
                atomindextoremovedipquad[atomidx]=True
            elif CheckIfAllAtomsSameClass(poltype,atomneighbs) and val==3: # then this is like Ammonia and we can use a trisector here which behaves like Z-only
                idxtotrisecbool[atomidx]=True
                trisectidxs=[atm.GetIdx() for atm in atomneighbs]
                idxtotrisectidxs[atomidx]=trisectidxs
                lfzerox[atomidx - 1]=True # need to zero out the x components just like for z-only case
        
            elif (val==2 and CheckIfAllAtomsSameClass(poltype,atomneighbs)) or (val==4 and len(uniqueneighbtypes)==2) and len(sorteduniquetypeneighbsnorepeat)==0:  # then this is like middle propane carbon or oxygen in water
                idxlist=GrabIndexesFromUniqueTypeNumber(poltype,atomneighbs,uniqueneighbtypes[0])
                poltype.localframe1[atomidx-1]=-1*idxlist[0]
                poltype.localframe2[atomidx-1]=-1*idxlist[1]
            elif len(uniqueneighbtypes)==2 and CheckIfNeighbHasSameType(poltype,atom,atomneighbs): # this handles, ethane,ethene...., z-only
                poltype.localframe1[atomidx-1]=sorteduniquetypeneighbsnorepeat[0]
                poltype.localframe2[atomidx - 1] = 0
                lfzerox[atomidx - 1]=True
        


            else:
                if len(sorteduniquetypeneighbsnorepeat)==1:
                    neighboffirstneighbs=[]
                    for n in openbabel.OBAtomAtomIter(highestsymneighbnorepeat):
                        neighboffirstneighbs.append(n)
                    newneighbs=RemoveFromList(poltype,neighboffirstneighbs,atom)
                    newsorteduniquetypeneighbsnorepeat=FindUniqueNonRepeatingNeighbors(poltype,newneighbs)
                    sorteduniquetypeneighbsnorepeat+=newsorteduniquetypeneighbsnorepeat
                poltype.localframe1[atomidx - 1]=sorteduniquetypeneighbsnorepeat[0]
                poltype.localframe2[atomidx - 1]=sorteduniquetypeneighbsnorepeat[1] 
    # write out the local frames
    iteratom = openbabel.OBMolAtomIter(mol)
    if not os.path.isfile(poltype.peditinfile):
        f = open (poltype.peditinfile, 'w')
        for a in iteratom:
            if not idxtobisecthenzbool[a.GetIdx()] and not idxtotrisecbool[a.GetIdx()]:
                f.write(str(a.GetIdx()) + " " + str(poltype.localframe1[a.GetIdx() - 1]) + " " + str(poltype.localframe2[a.GetIdx() - 1]) + "\n")
            elif idxtobisecthenzbool[a.GetIdx()] and not idxtotrisecbool[a.GetIdx()]:
                bisectidxs=idxtobisectidxs[a.GetIdx()]
                f.write(str(a.GetIdx()) + " " + str(poltype.localframe1[a.GetIdx() - 1]) + " -" + str(bisectidxs[0])+ " -" + str(bisectidxs[1]) + "\n")
            else:
                trisecidxs=idxtotrisectidxs[a.GetIdx()]
                f.write(str(a.GetIdx()) + " -" + str(trisecidxs[0])+ " -" + str(trisecidxs[1]) + " -" + str(trisecidxs[2])+ "\n")



        f.write("\n")
        f.write('A'+'\n')

        #Find aromatic carbon, halogens, and bonded hydrogens to correct polarizability
        iteratom = openbabel.OBMolAtomIter(mol)
        writesection=True
        lines=[]
        for index,prm in polarindextopolarizeprm.items():
           line=str(index)+' '+str(prm)+'\n'
           lines.append(line) 
        
        if writesection:
            for line in lines:
                f.write(line)

        


        f.write("\n")
        f.flush()
        os.fsync(f.fileno())
        f.write("2\n")
        f.write("N\n")
        f.write("Y\n")


        f.flush()
        os.fsync(f.fileno())

        f.close()
    


def rm_esp_terms_keyfile(poltype,keyfilename):
    """
    Intent: Remove unnecessary terms from the key file
    """
    tmpfname = keyfilename + "_tmp"
    temp=open(tmpfname,'w')
    anothertemp=open(keyfilename,'r')
    results=anothertemp.readlines()
    anothertemp.close()
    passedatomblock=False
    foundatomblock=False
    foundpolarize=False
    for line in results:
        if ('potential-offset' in line or 'none' in line or 'fix-monopole' in line) and 'atom' not in line:
            pass
        else:
            linesplit=line.split()
            if len(linesplit)>0:
                if linesplit[0]=='atom':
                    if foundatomblock==False:
                        foundatomblock=True
                    temp.write(line)

                else:
                    if foundatomblock==True:
                        passedatomblock=True
                    if linesplit[0]=='polarize':
                        foundpolarize=True
                    if passedatomblock==True and foundpolarize==False: # then old multipoles
                        pass
                    else:
                        temp.write(line)
            else:
                temp.write(line)

    temp.close()
    shutil.move(tmpfname, keyfilename)
   
    
def prepend_keyfile(poltype,keyfilename,optmol,dipole=False):
    """
    Intent: Adds a header to the key file given by 'keyfilename'
    """
    while not os.path.isfile(keyfilename):
        time.sleep(5)
        poltype.WriteToLog('Waiting for '+keyfilename)
    tmpfname = keyfilename + "_tmp"
    tmpfh = open(tmpfname, "w")
    keyfh = open(keyfilename, "r")
    tmpfh.write("parameters " + poltype.paramhead + "\n")
    tmpfh.write('OPENMP-THREADS '+str(poltype.numproc)+'\n')
    tmpfh.write("bondterm none\n")
    tmpfh.write("angleterm none\n")
    tmpfh.write("torsionterm none\n")
    tmpfh.write("vdwterm none\n")
    tmpfh.write("fix-monopole\n")
    tmpfh.write("digits 8\n")
    tmpfh.write("potential-offset 1.0\n")
    tmpfh.write("RESP-WEIGHT "+str(poltype.esprestweight)+"\n\n")


    logname=poltype.logespfname
    if poltype.fitqmdipole==True and os.path.exists(logname):
        qmdipole=esp.GrabQMDipoles(poltype,optmol,logname)
        tmpfh.write('TARGET-DIPOLE'+' '+str(qmdipole[0])+' '+str(qmdipole[1])+' '+str(qmdipole[2])+'\n')

    for line in keyfh:
        tmpfh.write(line)
    shutil.move(tmpfname, keyfilename)


def CheckFileForString(poltype,filetocheck):
    temp=open(filetocheck,'r')
    results=temp.readlines()
    temp.close()
    usemp2=False
    for line in results:
        if 'MP2' in line and 'Density' in line:
            usemp2=True
    if usemp2==False:
        string='CC'
    else:
        string='MP2'
    return string


def gen_gdmain(poltype,gdmainfname,molecprefix,fname,dmamethod):
    """
    Intent: Generate GDMA input file for the molecule
    Input:
        gdmainfname: file name for the gdma input file
        molecprefix: name of the molecule
        fname: file name for the *-dma.fchk file
    Output: *.gdmain file is created
    Referenced By: run_gdma
    Description:
        1. create pointer file dma.fchk to *-dma.fchk
        2. create *.gdmain file and write in all the necessary information for the gdma run
    """
    fnamesym = "dma.fchk"
    if not os.path.isfile(fnamesym):
        try:
            os.symlink(fname,fnamesym)
        except Exception as e:
            print(e)



    #punfname = os.path.splitext(fname)[0] + ".punch"
    punfname = "dma.punch"

    try:
        tmpfh = open(gdmainfname, "w")
    except IOError as e:
        print("I/O error({0}): {1}".format(e.errno, e.strerror))
        sys.exit(e.errno)

    tmpfh.write("Title " + molecprefix + " gdmain\n")
    tmpfh.write("\n")
    if poltype.dmamethod=='MP2':
        densitystring='MP2'
    else:
        densitystring='SCF'
    if poltype.dmamethod=='MP2':
        densitystring=CheckFileForString(poltype,fnamesym)
    tmpfh.write("File " + fnamesym  + " density %s\n"%(densitystring))
    tmpfh.write("Angstrom\n")
    tmpfh.write("AU\n")
    tmpfh.write("Multipoles\n")
    tmpfh.write("Switch 0\n") # v1.3, comment out for v2.2
    tmpfh.write("Limit 2\n")
    tmpfh.write("Punch " + punfname + "\n")
    tmpfh.write("Radius H 0.65\n")
    tmpfh.write("Radius S 0.80\n")
    tmpfh.write("Radius P 0.75\n")
    tmpfh.write("Radius Cl 1.0\n")
    tmpfh.write("Radius Br 1.1\n")
    tmpfh.write("Radius I 1.3\n")
    tmpfh.write("\n")
    tmpfh.write("Start\n")
    tmpfh.write("\n")
    tmpfh.write("Finish\n")
    tmpfh.close()

def run_gdma(poltype):
    """
    Intent: Runs GDMA to find multipole information
    The GDMA program carries out distributed multipole analysis of the wavefunctions
    calculated by Gaussian (using the *-dma.fchk file)
    Input:
    Output: *.gdmaout is created; this is used as input by poledit, a tinker program
    Referenced By: main
    Description:
    1. Generates the gdma input file by calling 'gen_gdmain'
    2. Runs the following command: gdma < *.gdmain > *.gdmaout
    """
    poltype.WriteToLog("NEED DMA: Executing GDMA")

    if not os.path.isfile(poltype.fckdmafname):
        poltype.fckdmafname = os.path.splitext(poltype.fckdmafname)[0]

    try:
        assert os.path.isfile(poltype.fckdmafname), "Error: " + poltype.fckdmafname + " does not exist."+' '+os.getcwd()
    except:
        poltype.DeleteFilesWithString(['dma'])
        poltype.GenerateParameters()

    poltype.gdmainfname = poltype.assign_filenames ( "gdmainfname" , ".gdmain")
    gen_gdmain(poltype,poltype.gdmainfname,poltype.molecprefix,poltype.fckdmafname,poltype.dmamethod)

    cmdstr = poltype.gdmaexe + " < " + poltype.gdmainfname + " > " + poltype.gdmafname
    poltype.call_subsystem(cmdstr,True)

    assert os.path.getsize(poltype.gdmafname) > 0, "Error: " + os.getcwd() +' '+os.path.basename(poltype.gdmaexe) + " cannot create .gdmaout file."
   
def AverageMultipoles(poltype,optmol):
    # gen input file
    gen_avgmpole_groups_file(poltype)
    # call avgmpoles.pl
    avgmpolecmdstr = poltype.avgmpolesexe + " " + poltype.keyfname + " " + poltype.xyzfname + " " + poltype.grpfname + " " + poltype.key2fname + " " + poltype.xyzoutfile + " " + str(poltype.prmstartidx)
    poltype.call_subsystem(avgmpolecmdstr,True)
    prepend_keyfile(poltype,poltype.key2fname,optmol,True)

def gen_avgmpole_groups_file(poltype):
    """
    Intent: Print out *-groups.txt which is a map from symm class to idx
    Also, symm class labels are altered from 1, 2, 3, ... to 401, 402, ...
    (or some other labeling system dependent on 'prmstartidx')
    Input:
    Output:
        *-groups.txt: map from symm group to atom idx
    Referenced By: main
    Description: -
    """
    symclasstoidxlist={}
    for idx,symclass in poltype.idxtosymclass.items():
        if symclass not in symclasstoidxlist.keys():
            symclasstoidxlist[symclass]=[]
        symclasstoidxlist[symclass].append(idx)
    f = open(poltype.grpfname,"w")
    for symclass,idxlist in symclasstoidxlist.items():
        string=str(symclass)+' '
        for idx in idxlist:
            string+=str(idx)+' '
        string+='\n'
        f.write(string)
    f.close()
