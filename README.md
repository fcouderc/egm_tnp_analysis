# egm_tnp_analysis


Package to handle analysis of tnp trees. The main tool is the python fitter

   ===> tnpEGM_fitter.py

The interface between the user and the fitter is solely done via the settings file

   ===> settings.py
   	- set the different samples and location
	- set the fitting bins
	- set the different cuts to be used
	- set the output directory

Help message:
>    python tnpEGM_fitter.py --help 

The settings has always to be pass to the fitter like this
>    python tnpEGM_fitter.py settings.py

This way different settings python can be setup or different WPs for instance


## the different fitting steps

**1. Create the bining.** To each bin is associated a cut that can be tuned bin by bin in the settings.py
   * After setting up the settings.py check bins 

>   python tnpEGM_fitter.py settings.py  --checkBins
   
   * if  you need additinal cuts for some bins (cleaning cuts), tune cuts in the settings.py, then recheck. 
     Once satisfied, create the bining

>   python tnpEGM_fitter.py settings.py  --createBins

   * CAUTION: when recreacting bins, the output directory is overwritten! So be sure to not redo that once really started

**2. Create the histograms** with the different cuts... this is the longest step. Histogram will not be re-done later
   
>   python tnpEGM_fitter.py settings.py --createHists

**3. Do your first step of fits.**
   * nominal fit
   
>   python tnpEGM_fitter.py settings.py --doFit
   
   * MC fit for alternate signal parameter constrain 
   
>   python tnpEGM_fitter.py settings.py --doFit --mcSig --altSig

   * Alternate signal fit (using constraints from previous fits)
   
>   python tnpEGM_fitter.py settings.py --doFit  --altSig

   * Alternate background fit (using constraints from previous fits)
   
>   python tnpEGM_fitter.py settings.py --doFit  --altBkg

**4. Check fits.** (there is a web index.php in the plot directory to vizualize from the web) and redo fit
   * can redo a given bin only via 
     the bin number ib can be found from --checkBins or in the ouput dir (or web interface)

>   python tnpEGM_fitter.py settings.py --doFit --iBin ib
   
   * the initial parameters can be tuned for this particular bin in the setting.py file. 
      Once the fit is good enough do not touch it do not redo all fits.
      One can redo any kind of fit bin by bin for instance the MC with alt model

>   python tnpEGM_fitter.py settings.py --doFit --mcSig --altSig --iBin ib

**5. egm txt ouput file.** Once all fits are fine, put everythin in the egm format txt file

>   python tnpEGM_fitter.py --sumUp
   
**6. Official egm output.** One can then do all the egm official control plots

>  python libPython/EGammaID_scaleFactors.py  <egamma.txtfile from step 5>


## The setting file

The setting file includes all the necessary information for a given setup of fit

**- General settings.**

    * flag: this is the Working point in the tnpTree  (pass: flag==1 ; fail flag==0)
    * baseOutDir: the output directory (will be created by the fitter)

**- Sample definition.**
    * tnpTreeDir: the directory in the tnpTree (different for phoID, eleID, reco, hlt)
    * samplesDef: these are the main info
        - data: data ntuple
	- mcNom: nominal MC sample
	- mcAlt: MC for generator syst
	- tagSel: usually same as nominal MC + different base cuts: check the tag selection syst
     For each samples
     	  - name: sample nickanme, used when storing the results 
	  - mcTruth: whether or not apply mcTruth when making histos
	  - cut: can have sample dependent cut but careful this is really mostly for the tag selection syst (or to restrict data in a given run range)
	  - path: path to the tnp tree with inputs (can use eos as in the example settings.py, but need to mount eos dir then)
 


====================
   


#### adding remote (Fabrice version)
git remote add origin git@github.com:fcouderc/egm_tnp_analysis.git