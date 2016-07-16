import ROOT as rt
rt.gROOT.LoadMacro('./libCpp/histFitter.C+')
rt.gROOT.LoadMacro('./libCpp/RooCBExGaussShape.cc+')
rt.gROOT.LoadMacro('./libCpp/RooCMSShape.cc+')
rt.gROOT.SetBatch(1)

from ROOT import tnpFitter

import re

def createWorkspaceForAltSig( info,  tnpBin, tnpWorkspaceParam ):

    ### tricky: use n < 0 for high pT bin (so need to remove param and add it back)
    cbNList = ['nP','nF']
    ptMin = -1
    if tnpBin['name'].find('pt_') >= 0:
        ptMin = float(tnpBin['name'].split('pt_')[1].split('p')[0])
    elif tnpBin['name'].find('et_') >= 0:
        ptMin = float(tnpBin['name'].split('et_')[1].split('p')[0])
    
    if ptMin >= 35 :
        for par in cbNList:
            for ip in range(len(tnpWorkspaceParam)):
                x=re.compile('%s.*?' % par)
                listToRM = filter(x.match, tnpWorkspaceParam)
                for ir in listToRM :
                    print '**** remove', ir
                    tnpWorkspaceParam.remove(ir)
                    
            tnpWorkspaceParam.append( '%s[-1,-3,-0.005]' % (par) )

                
        
    tnpWorkspaceFunc = [
        "RooCBExGaussShape::sigResPass(x,meanP,sigmaP,alphaP,nP, sigmaP_2)",
        "RooCBExGaussShape::sigResFail(x,meanF,sigmaF,alphaF,nF, sigmaF_2)",
        "RooCMSShape::bkgPass(x, acmsP, betaP, gammaP, peakP)",
        "RooCMSShape::bkgFail(x, acmsF, betaF, gammaF, peakF)",
        ]

    tnpWorkspace = []
    if not info['mcRef'] or info['mcTruth']:
        tnpWorkspace.extend(tnpWorkspaceParam)
        tnpWorkspace.extend(tnpWorkspaceFunc)        
        return tnpWorkspace

    
    fileref = info['mcRef'].replace('.root','.altSigFit.root')
    filemc = rt.TFile(fileref,'read')

    from ROOT import RooFit,RooFitResult
    fitresP = filemc.Get( '%s_resP' % tnpBin['name']  )
    fitresF = filemc.Get( '%s_resF' % tnpBin['name'] )

    listOfParam = ['nF','alphaF','nP','alphaP']
    
    fitPar = fitresF.floatParsFinal()
    for ipar in range(len(fitPar)):
        pName = fitPar[ipar].GetName()
        print '%s[%2.3f]' % (pName,fitPar[ipar].getVal())
        for par in listOfParam:
            if pName == par:
                print ' *** should remove param ', pName 
                x=re.compile('%s.*?' % pName)
                listToRM = filter(x.match, tnpWorkspaceParam)
                for ir in listToRM :
                    print '**** remove', ir
                    tnpWorkspaceParam.remove(ir)
                    
                tnpWorkspaceParam.append( '%s[%2.3f]' % (pName,fitPar[ipar].getVal()) )
                              
  
    fitPar = fitresP.floatParsFinal()
    for ipar in range(len(fitPar)):
        pName = fitPar[ipar].GetName()
        print '%s[%2.3f]' % (pName,fitPar[ipar].getVal())
        for par in listOfParam:
            if pName == par:
                x=re.compile('%s.*?' % pName)
                listToRM = filter(x.match, tnpWorkspaceParam)
                for ir in listToRM :
                    tnpWorkspaceParam.remove(ir)
                tnpWorkspaceParam.append( '%s[%2.3f]' % (pName,fitPar[ipar].getVal()) )
                
    filemc.Close()

    tnpWorkspace.extend(tnpWorkspaceParam)
    tnpWorkspace.extend(tnpWorkspaceFunc)        
    print tnpWorkspace
    return tnpWorkspace


#############################################################
########## nominal fitter
#############################################################
def histFitterNominal( info, tnpBin, tnpWorkspaceParam ):
        
    tnpWorkspaceFunc = [
        "Gaussian::sigResPass(x,meanP,sigmaP)",
        "Gaussian::sigResFail(x,meanF,sigmaF)",
        "RooCMSShape::bkgPass(x, acmsP, betaP, gammaP, peakP)",
        "RooCMSShape::bkgFail(x, acmsF, betaF, gammaF, peakF)",
        ]

    tnpWorkspace = []
    tnpWorkspace.extend(tnpWorkspaceParam)
    tnpWorkspace.extend(tnpWorkspaceFunc)

    
    ## init fitter
    infile = rt.TFile(info['infile'],"read")
    fitter = tnpFitter( infile, tnpBin['name']  )
    fitter.useMinos()
    infile.Close()
    rootfile = rt.TFile(info['infile'].replace('.root','.nominalFit.root'),'update')
    fitter.setOutputFile( rootfile )
    
    ## generated Z LineShape
    fileTruth = rt.TFile(info['mcRef'],'read')
    histZLineShapeP = fileTruth.Get('%s_Pass'%tnpBin['name'])
    histZLineShapeF = fileTruth.Get('%s_Fail'%tnpBin['name'])
    fitter.setZLineShapes(histZLineShapeP,histZLineShapeF)
    fileTruth.Close()

    ### set workspace
    workspace = rt.vector("string")()
    for iw in tnpWorkspace:
        workspace.push_back(iw)
    fitter.setWorkspace( workspace )

    title = tnpBin['title'].replace(';',' - ')
    title = title.replace('probe_sc_eta','#eta_{SC}')
    title = title.replace('probe_Ele_pt','p_{T}')
    fitter.fits(info['mcTruth'],title)
    rootfile.Close()



#############################################################
########## alternate signal fitter
#############################################################
def histFitterAltSig( info, tnpBin, tnpWorkspaceParam ):

    tnpWorkspace = createWorkspaceForAltSig( info,  tnpBin, tnpWorkspaceParam )
    
    ## init fitter
    infile = rt.TFile(info['infile'],'read')
    fitter = tnpFitter(infile, tnpBin['name']  )
    infile.Close()
    rootfile = rt.TFile(info['infile'].replace('.root','.altSigFit.root'),'update')
    fitter.setOutputFile( rootfile )

    
    ## generated Z LineShape
    fileTruth = rt.TFile('etc/inputs/ZeeGenLevel.root','read')
    histZLineShape = fileTruth.Get('Mass')
    fitter.setZLineShapes(histZLineShape,histZLineShape)
    fileTruth.Close()

    ### set workspace
    workspace = rt.vector("string")()
    for iw in tnpWorkspace:
        workspace.push_back(iw)
    fitter.setWorkspace( workspace )

    title = tnpBin['title'].replace(';',' - ')
    title = title.replace('probe_sc_eta','#eta_{SC}')
    title = title.replace('probe_Ele_pt','p_{T}')
    fitter.fits(info['mcTruth'],title)

    rootfile.Close()



#############################################################
########## alternate background fitter
#############################################################
def histFitterAltBkg( info, tnpBin, tnpWorkspaceParam ):

    tnpWorkspaceFunc = [
        "Gaussian::sigResPass(x,meanP,sigmaP)",
        "Gaussian::sigResFail(x,meanF,sigmaF)",
        "Exponential::bkgPass(x, alphaP)",
        "Exponential::bkgFail(x, alphaF)",
        ]

    tnpWorkspace = []
    tnpWorkspace.extend(tnpWorkspaceParam)
    tnpWorkspace.extend(tnpWorkspaceFunc)

    
    ## init fitter
    infile = rt.TFile(info['infile'],"read")
    fitter = tnpFitter( infile, tnpBin['name']  )
    infile.Close()
    rootfile = rt.TFile(info['infile'].replace('.root','.altBkgFit.root'),'update')
    fitter.setOutputFile( rootfile )
    
    ## generated Z LineShape
    fileTruth = rt.TFile(info['mcRef'],'read')
    histZLineShapeP = fileTruth.Get('%s_Pass'%tnpBin['name'])
    histZLineShapeF = fileTruth.Get('%s_Fail'%tnpBin['name'])
    fitter.setZLineShapes(histZLineShapeP,histZLineShapeF)
    fileTruth.Close()

    ### set workspace
    workspace = rt.vector("string")()
    for iw in tnpWorkspace:
        workspace.push_back(iw)
    fitter.setWorkspace( workspace )

    title = tnpBin['title'].replace(';',' - ')
    title = title.replace('probe_sc_eta','#eta_{SC}')
    title = title.replace('probe_Ele_pt','p_{T}')
    fitter.fits(info['mcTruth'],title)
    rootfile.Close()


