import copy

class tnpSample:
    def __init__(self, sName, path, cut = None, lumi = -1, nEvts = -1, mcTruth = False, puTree = None, isMC = False ):
        self.path = []
        self.name = sName
        self.path.append(path)
        self.cut     = cut
        self.lumi    = lumi
        self.nEvts   = nEvts
        self.mcTruth = mcTruth
        self.puTree  = puTree
        self.isMC    = isMC
        self.weight  = None
        
    def set_weight(self,weight):
        self.weight = weight

    def set_puTree(self,puTree):
        self.puTree = puTree

    def set_cut(self,cut):
        self.cut = cut
    
    def set_mcTruth(self,truth = True):
        self.mcTruth = truth

    def dump(self):
        print '**** name: %-*s ' % (100, self.name)
        print '  path   : ', self.path
        if self.isMC:
            print '   --- MC sample --- '
            print '  nEvts    : ', self.nEvts
            print '  mcTruth  : ', self.mcTruth
            print '  puTree   : ', self.puTree
            print '  weight   : ', self.weight
        else  :
            print '   --- Data sample --- '
            print '  lumi     : ', self.lumi

    def rename(self, newname):
        self.name = newname
    
    def clone(self):
        return copy.deepcopy(self)


    def addSample(self, sample):
        if self.lumi >= 0  :
            self.lumi = self.lumi + sample.lumi
        if self.nEvts >= 0 :
            self.nEvts = self.nEvts + sample.nEvts
        self.path.extend( sample.path )




import ROOT as rt
class tnpVarHist:
    def __init__(self, hname, var, title = None, xmin = -1, xmax = -1, nbins = -1 ):
        self.var   = var
        if title is None :  self.title = var
        else: self.title = title
        self.xmin  = xmin
        self.xmax  = xmax
        self.nbins = nbins
        self.hname = hname
        if nbins > 0:
            self.hist  = rt.TH1F( hname, title, nbin, xmin, xmax )
            self.hist.GetXaxis().SetTitle(title)
        else:
            self.hist = None

    def hist(self):
        return self.hist

