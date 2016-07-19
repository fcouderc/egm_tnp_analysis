import libPython.puReweighter as pu
import etc.inputs.tnpSampleDef as tnpSamples
        

for sName in tnpSamples.ICHEP2016.keys():
    sample = tnpSamples.ICHEP2016[sName]
    if sample is None : continue
    if not sample.isMC: continue
    sample.set_puTree( 'etc/inputs/ichep2016/%s.puTree.root' % sample.name )
    sample.dump()
    pu.reweight(sample)
    
