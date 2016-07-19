import libPython.puReweighter as pu
from libPython.tnpSampleUtils import *
import etc.inputs.tnpSampleDef as tnpSamples
        

for sName in tnpSamples.ICHEP2016.keys():
    sample = tnpSamples.ICHEP2016[sName]
    if not sample is None:    sample.dump()
    
