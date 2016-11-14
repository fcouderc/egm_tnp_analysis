import libPython.puReweighter as pu
import etc.inputs.tnpSampleDef as tnpSamples
from libPython.tnpClassUtils import mkdir


puType = 2

for sName in tnpSamples.Moriond17_80X.keys():    
    sample = tnpSamples.Moriond17_80X[sName]
    if sample is None : continue
    if not sample.isMC: continue
    
    trees = {}
#    trees['ele'] = 'GsfElectronToEleID'
    trees['pho'] = 'GsfElectronToPhoID'
    for tree in trees:
        dirout =  'etc/inputs/moriond17/'
        mkdir(dirout)
        
        if   puType == 0 : sample.set_puTree( dirout + '%s_%s.pu.puTree.root'  % (sample.name,tree) )
        elif puType == 1 : sample.set_puTree( dirout + '%s_%s.nVtx.puTree.root' % (sample.name,tree) )
        elif puType == 2 : sample.set_puTree( dirout + '%s_%s.rho.puTree.root'  % (sample.name,tree) )
        sample.set_tnpTree(trees[tree]+'/fitter_tree')
        sample.dump()
        pu.reweight(sample, puType )
    
