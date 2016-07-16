#############################################################
########## General settings
#############################################################
# flag to be Tested
flags = {
    'passingLoose'  : '(passingLoose  == 1)',
    'passingMedium' : '(passingMedium == 1)',
    'passingTight'  : '(passingTight  == 1)',
    'passingMVA'    : '(passingMVA  == 1)',
    }
baseOutDir = 'resultsPhoID/runB/'

#############################################################
########## samples definition  [can be nD bining]
#############################################################
tnpTreeDir = 'GsfElectronToPhoID'
weightName = 'totWeight'

### MANDATORY nEvts in data = -1 // mcTruth will require mc Matching
## some sample based cuts... general cuts defined here after
cutAltSel = 'tag_Ele_pt > 33  && tag_Ele_nonTrigMVA > 0.90'
cutData   = None 
direos    = 'eos/cms/store/group/phys_egamma/tnp/80X/Photons_76Xids/phov2/'
samplesDef = {
    'data'      : { 'name' :  'data_2016_runB' , 'mcTruth' : False, 'nEvts':       -1, 'cut' : cutData,
                    'path' :  '%s/data/TnPTree_SingleElectron_2016_RunB.root' % direos  },
    'mcNom'     : { 'name' : 'mcMadgraph80XNom'   , 'mcTruth' : True , 'nEvts': 36311064, 'cut' : None,
                    'path' : '%s/mc/TnPTree_DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root' % direos },
    'mcAlt'     : { 'name' : 'mcAtNLO80XNom'      , 'mcTruth' : True , 'nEvts': 36311064, 'cut' : None,
                    'path' : '%s/mc/TnPTree_DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8.root'% direos },
    'tagSel'    : { 'name' : 'mcMadgraph80XAltSel', 'mcTruth' : True , 'nEvts': 36311064, 'cut': cutAltSel,
                    'path' : '%s/mc/TnPTree_DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root' % direos },
}

### lumi in /fb
lumi = 5.657

#############################################################
########## bining definition  [can be nD bining]
#############################################################
biningDef = [
   { 'var' : 'probe_sc_eta' , 'type': 'float', 'bins': [-2.5,-2.0,-1.566,-1.4442, -1.0, 0.0, 1.0, 1.4442, 1.566, 2.0, 2.5] },
   { 'var' : 'probe_Pho_et' , 'type': 'float', 'bins': [20.0,30,40,50,200] },
]

#############################################################
########## Cuts definition for all samples
#############################################################
### cut
cutBase   = 'tag_Ele_pt > 30 && abs(tag_sc_eta) < 2.1'

# can add addtionnal cuts for some bins (first check bin number using tnpEGM --checkBins)
additionalCuts = { 
    0 : 'tag_Ele_trigMVA > 0.92 && sqrt( 2*event_met_pfmet*tag_Ele_pt*(1-cos(event_met_pfphi-tag_Ele_phi))) < 45',
    1 : 'tag_Ele_trigMVA > 0.92 && sqrt( 2*event_met_pfmet*tag_Ele_pt*(1-cos(event_met_pfphi-tag_Ele_phi))) < 45',
    2 : 'tag_Ele_trigMVA > 0.92 && sqrt( 2*event_met_pfmet*tag_Ele_pt*(1-cos(event_met_pfphi-tag_Ele_phi))) < 45',
    3 : 'tag_Ele_trigMVA > 0.92 && sqrt( 2*event_met_pfmet*tag_Ele_pt*(1-cos(event_met_pfphi-tag_Ele_phi))) < 45',
    4 : 'tag_Ele_trigMVA > 0.92 && sqrt( 2*event_met_pfmet*tag_Ele_pt*(1-cos(event_met_pfphi-tag_Ele_phi))) < 45',
    5 : 'tag_Ele_trigMVA > 0.92 && sqrt( 2*event_met_pfmet*tag_Ele_pt*(1-cos(event_met_pfphi-tag_Ele_phi))) < 45',
    6 : 'tag_Ele_trigMVA > 0.92 && sqrt( 2*event_met_pfmet*tag_Ele_pt*(1-cos(event_met_pfphi-tag_Ele_phi))) < 45',
    7 : 'tag_Ele_trigMVA > 0.92 && sqrt( 2*event_met_pfmet*tag_Ele_pt*(1-cos(event_met_pfphi-tag_Ele_phi))) < 45',
    8 : 'tag_Ele_trigMVA > 0.92 && sqrt( 2*event_met_pfmet*tag_Ele_pt*(1-cos(event_met_pfphi-tag_Ele_phi))) < 45',
    9 : 'tag_Ele_trigMVA > 0.92 && sqrt( 2*event_met_pfmet*tag_Ele_pt*(1-cos(event_met_pfphi-tag_Ele_phi))) < 45'
}

#### or remove any additional cut (default)
#additionalCuts = None

#############################################################
########## fitting params to tune fit by hand if necessary
#############################################################
tnpParNomFit = [
    "meanP[-0.0,-5.0,5.0]","sigmaP[0.5,0.1,5.0]",
    "meanF[-0.0,-5.0,5.0]","sigmaF[0.5,0.1,5.0]",
    "acmsP[60.,50.,80.]","betaP[0.05,0.01,0.08]","gammaP[0.1, 0, 1]","peakP[90.0]",
    "acmsF[60.,50.,80.]","betaF[0.05,0.01,0.08]","gammaF[0.1, 0, 1]","peakF[90.0]",
    ]

tnpParAltSigFit = [
    "meanP[-0.0,-5.0,5.0]","sigmaP[1,0.7,6.0]" ,"alphaP[2.0,0.8,3.5]" ,'nP[3,0.05,5]',"sigmaP_2[1.5,0.5,6.0]",
    "meanF[-0.0,-5.0,5.0]","sigmaF[2,0.7,15.0]","alphaF[2.0,0.8,3.5]",'nF[3,0.05,5]',"sigmaF_2[2.0,0.5,6.0]",
    "acmsP[60.,50.,75.]","betaP[0.04,0.01,0.06]","gammaP[0.1, 0.005, 1]","peakP[90.0]",
    "acmsF[60.,50.,75.]","betaF[0.04,0.01,0.06]","gammaF[0.1, 0.005, 1]","peakF[90.0]",
    ]
     
tnpParAltBkgFit = [
    "meanP[-0.0,-5.0,5.0]","sigmaP[0.5,0.1,5.0]",
    "meanF[-0.0,-5.0,5.0]","sigmaF[0.5,0.1,5.0]",
    "alphaP[0.,-5.,5.]",
    "alphaF[0.,-5.,5.]",
    ]
        
