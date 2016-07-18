#!bin/bash 

## install gcc 4.9
optVer=x86_64-slc6-gcc49-opt
optVer=x86_64-slc6-gcc48-opt

## install modern version of ROOT
LCG=/afs/cern.ch/sw/lcg/
ROOTSYS=$LCG/app/releases/ROOT/6.06.06/$optVer/root/
. $LCG/external/gcc/4.8.0/$optVer/setup.sh
. $ROOTSYS/bin/thisroot.sh

## add python lib
. /opt/rh/python27/enable
#export PYTHONDIR=/afs/cern.ch/sw/lcg/external/Python/2.7.3/$optVer
#export LD_LIBRARY_PATH=$ROOTSYS/lib:$PYTHONDIR/lib:$LD_LIBRARY_PATH:/opt/rh/python27/root/usr/lib64
#export PYTHONPATH=$PYTHONPATH:$ROOTSYS/lib
#export PATH=$PYTHONDIR/bin:$PATH