
### python specific import
import argparse
import os
import sys
import pickle
import shutil


parser = argparse.ArgumentParser(description='tnp EGM fitter')
parser.add_argument('--checkBins'  , action='store_true'  , help='check  bining definition')
parser.add_argument('--createBins' , action='store_true'  , help='create bining definition')
parser.add_argument('--createHists', action='store_true'  , help='create histograms')
parser.add_argument('--altSig'     , action='store_true'  , help='alternate signal model fit')
parser.add_argument('--altBkg'     , action='store_true'  , help='alternate background model fit')
parser.add_argument('--doFit'      , action='store_true'  , help='fit sample (sample should be defined in settings.py)')
parser.add_argument('--mcSig'      , action='store_true'  , help='fit MC nom [to init fit parama]')
parser.add_argument('--doPlot'     , action='store_true'  , help='plotting')
parser.add_argument('--sumUp'      , action='store_true'  , help='sum up efficiencies')
parser.add_argument('--iBin'       , dest = 'binNumber'   , type = int,  default=-1, help='bin number (to refit individual bin)')
parser.add_argument('settings'     , default = None       , help = 'setting file [mandatory]')

args = parser.parse_args()
print args
importSetting = 'import %s as tnpConf' % args.settings.split('.py')[0]
exec(importSetting)

### tnp library
import libPython.binUtils  as tnpBiner
import libPython.rootUtils as tnpRoot


#### Creating and/or loading the bining 
if args.checkBins:
    tnpBins = tnpBiner.createBins(tnpConf.biningDef,tnpConf.cutBase)
    tnpBiner.tuneCuts( tnpBins, tnpConf.additionalCuts )
    for ib in range(len(tnpBins['bins'])):
        print tnpBins['bins'][ib]['name']
        print '  - cut: ',tnpBins['bins'][ib]['cut']
    sys.exit(0)
    
if args.createBins:
    if os.path.exists( tnpConf.baseOutDir ):
            shutil.rmtree( tnpConf.baseOutDir )
    os.makedirs( tnpConf.baseOutDir )
    tnpBins = tnpBiner.createBins(tnpConf.biningDef,tnpConf.cutBase)
    tnpBiner.tuneCuts( tnpBins, tnpConf.additionalCuts )
    pickle.dump( tnpBins, open( '%s/bining.pkl'%(tnpConf.baseOutDir),'wb') )
    print 'created dir: %s ' % tnpConf.baseOutDir
    print 'bining created successfully... '
    print 'Note than any additional call to createBins will overwrite directory %s' % tnpConf.baseOutDir
    sys.exit(0)

tnpBins = pickle.load( open( '%s/bining.pkl'%(tnpConf.baseOutDir),'rb') )

####################################################################
##### Create Histograms
####################################################################
if args.createHists:
    for sampleType in tnpConf.samplesDef.keys():
        sample =  tnpConf.samplesDef[sampleType]
        if sample is None : continue
        print 'creating histogram for sample %s' % sample['name']
        isMC = True
        if sample['nEvts'] < 0 : isMC = False
        info = {
            'infile'  : sample['path'],
            'outfile' : '%s/%s_%s.root' % ( tnpConf.baseOutDir ,sample['name'], tnpConf.flag ),
            'tree'    : '%s/fitter_tree'% tnpConf.tnpTreeDir,
            'weight'  : tnpConf.weightName,
            'flag'    : tnpConf.flag,
            'cut'     : sample['cut'],
            'mcTruth' : sample['mcTruth'],
            'isMC'    : isMC
        }
        var = { 'name' : 'pair_mass', 'nbins' : 60, 'min' : 60, 'max': 120 }
        tnpRoot.makePassFailHistograms( info, tnpBins, var )
    sys.exit(0)


sample = tnpConf.samplesDef['data']
if args.mcSig :
    sample = tnpConf.samplesDef['mcNom']
if sample is None:
    print '[FITTER]: sample (data or MC) not available... check histograming step'
    sys.exit(1)
sampleMC = tnpConf.samplesDef['mcNom']
if sampleMC is None:
    print '[FITTER]: MC sample not available... check histograming step'
    sys.exit(1)



####################################################################
##### Actual Fitter
####################################################################
if  args.doFit:

    isMC = True
    if sample['nEvts'] < 0 :
        isMC = False
        
    info = {
        'infile' : '%s/%s_%s.root' % ( tnpConf.baseOutDir ,  sample['name'], tnpConf.flag ),
        'tree'    : '%s/fitter_tree'% tnpConf.tnpTreeDir,
        'weight'  : tnpConf.weightName,
        'flag'    : tnpConf.flag,
        'mcTruth' : sample['mcTruth'],
        'isMC'    : isMC,
        'mcRef'   : None
        }

    info['mcRef'] = '%s/%s_%s.root' % ( tnpConf.baseOutDir ,  sampleMC['name'], tnpConf.flag )
        
    if args.binNumber == -1:
        for ib in range(len(tnpBins['bins'])):
            if args.altSig:                 
                tnpRoot.histFitterAltSig(  info, tnpBins['bins'][ib], tnpConf.tnpParAltSigFit )
            elif args.altBkg:
                tnpRoot.histFitterAltBkg(  info, tnpBins['bins'][ib], tnpConf.tnpParAltBkgFit )
            else:
                tnpRoot.histFitterNominal( info, tnpBins['bins'][ib], tnpConf.tnpParNomFit )
    else:
        ib = args.binNumber
        if args.altSig:                
            tnpRoot.histFitterAltSig(  info, tnpBins['bins'][ib], tnpConf.tnpParAltSigFit )
        elif args.altBkg:
            tnpRoot.histFitterAltBkg(  info, tnpBins['bins'][ib], tnpConf.tnpParAltBkgFit )
        else:
            tnpRoot.histFitterNominal( info, tnpBins['bins'][ib], tnpConf.tnpParNomFit )

    args.doPlot = True
     
####################################################################
##### dumping plots
####################################################################
if  args.doPlot:
    fitType = 'nominalFit'
    if args.altSig : fitType = 'altSigFit'
    if args.altBkg : fitType = 'altBkgFit'
        
    plottingDir = '%s/plots/%s/%s' % (tnpConf.baseOutDir,sample['name'],fitType)
    if not os.path.exists( plottingDir ):
        os.makedirs( plottingDir )
    shutil.copy('data/index.php.listPlots','%s/index.php' % plottingDir)

    isMC = True
    if sample['nEvts'] < 0 : isMC = False
    info = {
        'outfile' : '%s/%s_%s.%s.root' % ( tnpConf.baseOutDir,sample['name'], tnpConf.flag,fitType ),
        'flag'    : tnpConf.flag,
        'mcTruth' : sample['mcTruth'],
        'isMC'    : isMC,
        'plotDir' : plottingDir
    }        
    
    if args.binNumber == -1:
        for ib in range(len(tnpBins['bins'])):
            tnpRoot.histPlotter( info, tnpBins['bins'][ib] )
    else:
        tnpRoot.histPlotter( info, tnpBins['bins'][args.binNumber] )

    print ' ===> Plots saved in <======='
    print 'localhost/%s/' % plottingDir


####################################################################
##### dumping egamma txt file 
####################################################################
if args.sumUp:
    info = {
        'dataNominal' : '%s/%s_%s.%s.root' % ( tnpConf.baseOutDir , tnpConf.samplesDef['data' ]['name'], tnpConf.flag, 'nominalFit' ),
        'dataAltSig'  : '%s/%s_%s.%s.root' % ( tnpConf.baseOutDir , tnpConf.samplesDef['data' ]['name'], tnpConf.flag, 'altSigFit'  ),
        'dataAltBkg'  : '%s/%s_%s.%s.root' % ( tnpConf.baseOutDir , tnpConf.samplesDef['data' ]['name'], tnpConf.flag, 'altBkgFit'  ),
        'mcNominal'   : '%s/%s_%s.root' % ( tnpConf.baseOutDir , tnpConf.samplesDef['mcNom']['name'], tnpConf.flag ),
        'mcAlt'       : None,
        'tagSel'      : None
        }

    if not tnpConf.samplesDef['mcAlt' ] is None:
        info['mcAlt'    ] = '%s/%s_%s.root'  % ( tnpConf.baseOutDir , tnpConf.samplesDef['mcAlt' ]['name'] , tnpConf.flag )
    if not tnpConf.samplesDef['tagSel'] is None:
        info['tagSel'   ] = '%s/%s_%s.root'  % ( tnpConf.baseOutDir , tnpConf.samplesDef['tagSel']['name'] , tnpConf.flag )

    effis = None
    effFileName ='%s/egammaEffi.txt' % tnpConf.baseOutDir 
    fOut = open( effFileName,'w')
    
    for ib in range(len(tnpBins['bins'])):
        effis = tnpRoot.getAllEffi( info, tnpBins['bins'][ib] )

        ### formatting assuming 2D bining -- to be fixed        
        v1Range = tnpBins['bins'][ib]['title'].split(';')[1].split('<')
        v2Range = tnpBins['bins'][ib]['title'].split(';')[2].split('<')
        if ib == 0 :
            fOut.write( '### var1 : %s\n' % v1Range[1])
            fOut.write( '### var2 : %s\n' % v2Range[1] )
            
        fOut.write( '%1.3f\t%1.3f\t%1.3f\t%1.3f\t%1.3f\t%1.3f\t%1.3f\t%1.3f\t%1.3f\t%1.3f\t%1.3f\t%1.3f\n' % (
            float(v1Range[0]), float(v1Range[2]),
            float(v2Range[0]), float(v2Range[2]),
            effis['dataNominal'][0],effis['dataNominal'][1],
            effis['mcNominal'  ][0],effis['mcNominal'  ][1],
            effis['dataAltSig' ][0],
            effis['dataAltBkg' ][0],
            effis['mcAlt' ][0],
            effis['tagSel'][0],
            )
            )
    fOut.close()

    print 'Effis saved in file : ',  effFileName
