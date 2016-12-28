import ROOT as rt
import numpy as np
import sys
import argparse
import os

print '** puReweighter requires root_numpy.'
print '** To install on lxplus: '
print 'pip install --user root_numpy'
from root_numpy import  tree2array, array2tree


puMC = {
    'Spring2016MC_PUscenarioV1' : [ 0.000829312873542, 0.00124276120498, 0.00339329181587, 0.00408224735376, 0.00383036590008, 
                                    0.00659159288946,  0.00816022734493, 0.00943640833116, 0.0137777376066,  0.017059392038,
                                    0.0213193035468,   0.0247343174676,  0.0280848773878,  0.0323308476564,  0.0370394341409,  
                                    0.0456917721191,   0.0558762890594,  0.0576956187107,  0.0625325287017,  0.0591603758776,
                                    0.0656650815128,   0.0678329011676,  0.0625142146389,  0.0548068448797,  0.0503893295063,  
                                    0.040209818868,    0.0374446988111,  0.0299661572042,  0.0272024759921,  0.0219328403791,
                                    0.0179586571619,   0.0142926728247,  0.00839941654725, 0.00522366397213, 0.00224457976761, 
                                    0.000779274977993, 0.000197066585944,7.16031761328e-05,0.0             , 0.0,
                                    0.0,        0.0,        0.0,        0.0,        0.0,    
                                    0.0,        0.0,        0.0,        0.0,        0.0],
    
    'Moriond17MC_mix_2016'      : [ 1.78653e-05 ,2.56602e-05 ,5.27857e-05 ,8.88954e-05 ,0.000109362 ,0.000140973 ,0.000240998 ,
                                    0.00071209  , 0.00130121 ,0.00245255  ,0.00502589  ,0.00919534  ,0.0146697   ,0.0204126   ,
                                    0.0267586   ,0.0337697   ,0.0401478   ,0.0450159   ,0.0490577   ,0.0524855   ,0.0548159   ,
                                    0.0559937   ,0.0554468   ,0.0537687   ,0.0512055   ,0.0476713   ,0.0435312   ,0.0393107   ,
                                    0.0349812   ,0.0307413   ,0.0272425   ,0.0237115   ,0.0208329   ,0.0182459   ,0.0160712   ,
                                    0.0142498   ,0.012804    ,0.011571    ,0.010547    ,0.00959489  ,0.00891718  ,0.00829292  , 
                                    0.0076195   ,0.0069806   ,0.0062025   ,0.00546581  ,0.00484127  ,0.00407168  ,0.00337681  ,
                                    0.00269893  ,0.00212473  ,0.00160208  ,0.00117884  ,0.000859662 ,0.000569085 ,0.000365431 ,
                                    0.000243565 ,0.00015688  ,9.88128e-05 ,6.53783e-05 ,3.73924e-05 ,2.61382e-05 ,2.0307e-05  ,
                                    1.73032e-05 ,1.435e-05   ,1.36486e-05 ,1.35555e-05 ,1.37491e-05 ,1.34255e-05 ,1.33987e-05 ,
                                    1.34061e-05 ,1.34211e-05 ,1.34177e-05 ,1.32959e-05 ,1.33287e-05 ],
}

### MC pu scenario to be used
#puMCscenario = 'Spring2016MC_PUscenarioV1'
puMCscenario = 'Moriond17MC_mix_2016'
puDirEOS = 'eos/cms//store/group/phys_egamma/tnp/80X/pu/'

#### Compute weights for all data epoch specified below
puDataEpoch = {
    '2016_runBCD' : puDirEOS + 'pu_dist_runBCD_692.root',
    '2016_runEF'  : puDirEOS + 'pu_dist_runEF_692.root' ,
    '2016_runGH'  : puDirEOS + 'pu_dist_runGH_692.root' ,
    '2016_runAll' : puDirEOS + 'pu_dist_run2016_692.root',    
}

nVtxDataEpoch = {
    '2016_runBCD' : 'etc/inputs/nVtx_2016_runBCD.root',
    '2016_runEF'  : 'etc/inputs/nVtx_2016_runEF.root' ,
    '2016_runGH'  : 'etc/inputs/nVtx_2016_runGH.root' ,
}

rhoDataEpoch = {
    '2016_runE'   : 'etc/inputs/rho_pu_runE.root',
    '2016_runGH'  : 'etc/inputs/rho_pu_runGH.root',
}





def reweight( sample, puType = 0  ):
    if sample.path is None:
        print '[puReweighter]: Need to know the MC tree (option --mcTree or sample.path)'
        sys.exit(1)
    

### create a tree with only weights that will be used as friend tree for reweighting different lumi periods
    print 'Opening mc file: ', sample.path[0]
    fmc = rt.TFile(sample.path[0],'read')
    tmc = None
    if sample.tnpTree is None:
        dirs = fmc.GetListOfKeys()
        for d in dirs:
            if (d.GetName() == "sampleInfo"): continue
            tmc = fmc.Get("%s/fitter_tree" % d.GetName())
    else:
        tmc = fmc.Get(sample.tnpTree)
    

#### can reweight vs nVtx but better to reweight v truePU
    puMCnVtx = []
    puMCrho = []
    if   puType == 1 :
        hmc   = rt.TH1F('hMC_nPV'  ,'MC nPV'  , 75,-0.5,74.5)
        tmc.Draw('event_nPV>>hMC_nPV','','goff')
        hmc.Scale(1/hmc.Integral())
        for ib in range(1,hmc.GetNbinsX()+1):
            puMCnVtx.append( hmc.GetBinContent(ib) )
        print 'len nvtxMC = ',len(puMCnVtx)

    elif puType == 2 :
        hmc   = rt.TH1F('hMC_rho'  ,'MC #rho'  , 75,-0.5,74.5)
        tmc.Draw('rho>>hMC_rho','','goff')
        hmc.Scale(1/hmc.Integral())
        for ib in range(1,hmc.GetNbinsX()+1):
            puMCrho.append( hmc.GetBinContent(ib) )
        print 'len rhoMC = ',len(puMCrho)
    

    puDataDist = {}
    puDataArray= {}
    weights = {}
    epochKeys = puDataEpoch.keys()
    if puType == 1  : epochKeys = nVtxDataEpoch.keys()
    if puType == 2  : epochKeys = rhoDataEpoch.keys()
 
    for pu in epochKeys:
        fpu = None
        if   puType == 1 : fpu = rt.TFile(nVtxDataEpoch[pu],'read')
        elif puType == 2 : fpu = rt.TFile(rhoDataEpoch[pu],'read')
        else             : fpu = rt.TFile(puDataEpoch[pu],'read')
        puDataDist[pu] = fpu.Get('pileup').Clone('puHist_%s' % pu)
        puDataDist[pu].Scale(1./puDataDist[pu].Integral())
        puDataDist[pu].SetDirectory(0)
        puDataArray[pu] = []
        for ipu in range(len(puMC[puMCscenario])):
            ibin_pu  = puDataDist[pu].GetXaxis().FindBin(ipu+0.00001)
            puDataArray[pu].append(puDataDist[pu].GetBinContent(ibin_pu))
        print 'puData[%s] length = %d' % (pu,len(puDataArray[pu]))
        fpu.Close()
        weights[pu] = []

    mcEvts = tree2array( tmc, branches = ['weight','truePU','event_nPV','rho'] )


    pumc = puMC[puMCscenario]
    if   puType == 1:  pumc = puMCnVtx
    elif puType == 2:  pumc = puMCrho
    else            :  pumc = puMC[puMCscenario]

    puMax = len(pumc)
    print '-> nEvtsTot ', len(mcEvts)
    for ievt in xrange(len(mcEvts)):
        if ievt%1000000 == 0 :            print 'iEvt:',ievt
        evt = mcEvts[ievt]
        for pu in epochKeys:
            pum = -1
            pud = -1
            if puType == 1 and evt['event_nPV'] < puMax:
                pud = puDataArray[pu][evt['event_nPV']]
                pum = pumc[evt['event_nPV']]
            if puType == 2 and int(evt['rho']) < puMax:
                pud = puDataArray[pu][int(evt['rho'])]
                pum = pumc[int(evt['rho'])]
            elif puType == 0:
                pud = puDataArray[pu][evt['truePU']] 
                pum = pumc[evt['truePU']]
            puw = 1
            if pum > 0: 
                puw  = pud/pum

            if evt['weight'] > 0 : totw = +puw
            else                 : totw = -puw
            weights[pu].append( ( puw,totw) )

    newFile    = rt.TFile( sample.puTree, 'recreate')

    for pu in epochKeys:
        treeWeight = rt.TTree('weights_%s'%pu,'tree with weights')
        wpuarray = np.array(weights[pu],dtype=[('PUweight',float),('totWeight',float)])
        array2tree( wpuarray, tree = treeWeight )
        treeWeight.Write()

    newFile.Close()    
    fmc.Close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='tnp EGM pu reweighter')
    parser.add_argument('--mcTree'  , dest = 'path',  default = None, help = 'MC tree to compute weights for')
    parser.add_argument('puTree'    , default = None                , help = 'output puTree')

    args = parser.parse_args()
    args.path = [args.path]
    reweight(args)





