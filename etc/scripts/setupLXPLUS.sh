#!bin/bash 

## install gcc 4.9
optVer=x86_64-slc6-gcc49-opt

## install modern version of ROOT
ROOTSYS=$LCG/app/releases/ROOT/6.06.06/$optVer/root/
. $LCG/external/gcc/4.9.0/$optVer/setup.sh
. $ROOTSYS/bin/thisroot.sh

## add python lib
export LD_LIBRARY_PATH=/opt/rh/python27/root/usr/lib64/:$LD_LIBRARY_PATH