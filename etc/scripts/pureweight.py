import libPython.puReweighter as pu
import etc.inputs.tnpSampleDef as tnpSamples
        

for sName in tnpSamples.ICHEP2016.keys():
    
    sample = tnpSamples.ICHEP2016[sName]
    if sName == 'mc_DY_madgraph_ele': continue
    if sName == 'mc_DY_amcatnlo_ele': continue
    if sName == 'mc_DY_amcatnlo_rec': continue
#    if sName == 'mc_DY_madgraph_rec': continue
#    if sName == 'mc_DY_madgraph_pho': continue
#    if sName == 'mc_DY_amcatnlo_pho': continue

    if sample is None : continue
    if not sample.isMC: continue
    sample.set_puTree( 'etc/inputs/ichep2016/%s.puTree.root' % sample.name )
    sample.dump()
    pu.reweight(sample,True)
    
