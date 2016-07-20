from libPython.tnpClassUtils import tnpSample


eosDir = 'eos/cms/store/group/phys_egamma/tnp/80X/'


ICHEP2016 = {
    'mc_DY_madgraph_ele' : tnpSample('mc_DY_madgraph_ele', eosDir + 'Photons_76Xids/elev2/mc/TnPTree_DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root' , isMC = True, nEvts = 36311064 ),
    'mc_DY_amcatnlo_ele' : tnpSample('mc_DY_amcatnlo_ele', eosDir + 'Photons_76Xids/elev2/mc/TnPTree_DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8.root', isMC = True, nEvts = 28696958 ),
    'mc_DY_madgraph_pho' : tnpSample('mc_DY_madgraph_pho', eosDir + 'Photons_76Xids/phov2/mc/TnPTree_DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root' , isMC = True, nEvts = 41253879 ),
    'mc_DY_amcatnlo_pho' : tnpSample('mc_DY_amcatnlo_pho', eosDir + 'Photons_76Xids/phov2/mc/TnPTree_DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8.root', isMC = True, nEvts = 28696958 ),
    'mc_DY_madgraph_rec' : tnpSample('mc_DY_madgraph_rec', eosDir + 'RecoSF/RECOv3/mc//TnPTree_DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root'       , isMC = True, nEvts = 49877138 ),
    'mc_DY_amcatnlo_rec' : tnpSample('mc_DY_amcatnlo_rec', eosDir + 'RecoSF/RECOv3/mc//TnPTree_DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8.root'      , isMC = True, nEvts = 28328619 ),

    'data_2016_runB_ele' :  tnpSample('data_2016_runB_ele', eosDir + 'Photons_76Xids/elev2/data/TnPTree_SingleElectron_2016_RunB.root' , lumi = 5.709 ),
    'data_2016_runC_ele' :  tnpSample('data_2016_runC_ele', eosDir + 'Photons_76Xids/elev3/data/TnPTree_SingleElectron_2016_RunC.root' , lumi = 2.646 ),
    'data_2016_runD_ele' :  tnpSample('data_2016_runD_ele', eosDir + 'Photons_76Xids/elev3/data/TnPTree_SingleElectron_2016_RunD.root' , lumi = 4.330 ),
    'data_2016_runB_pho' :  tnpSample('data_2016_runB_pho', eosDir + 'Photons_76Xids/phov2/data/TnPTree_SingleElectron_2016_RunB.root' , lumi = 5.900 ),
    'data_2016_runC_pho' :  tnpSample('data_2016_runC_pho', eosDir + 'Photons_76Xids/phov3/data/TnPTree_SingleElectron_2016_RunC.root' , lumi = 2.646 ),
    'data_2016_runD_pho' :  tnpSample('data_2016_runD_pho', eosDir + 'Photons_76Xids/phov3/data/TnPTree_SingleElectron_2016_RunD.root' , lumi = 4.330 ),
    'data_2016_runB_rec' :  tnpSample('data_2016_runB_rec', eosDir + 'RecoSF/RECOv3/data//TnPTree_SingleElectron_2016_RunB.root'       , lumi = 5.237 ),
    'data_2016_runC_rec' :  tnpSample('data_2016_runC_rec', eosDir + 'RecoSF/RECOv4/data//TnPTree_SingleElectron_2016_RunC.root'       , lumi = 2.646 ),
    'data_2016_runD_rec' :  None,
}
