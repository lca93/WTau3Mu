# WTau3Mu
## CMSSW setup
Setup a consistent release of CMSSW (9_4_X for 2017, 10_2_X for 2018)
```
cmsrel CMSSW_X_X_X
cd CMSSW_X_X_X/src
cmsenv
git cms-init
git cms-addpkg PhysicsTools/Heppy
git cms-addpkg PhysicsTools/HeppyCore
git cms-addpkg RecoEgamma
git cms-addpkg RecoTauTag/RecoTau
scram b -j 8
```
## follow [CMGTools](https://github.com/CERN-PH-CMG/cmgtools-lite) installation, then clone this package into `$CMSSW_BASE/src/CMGTools`  

## install a recent version of scikit learn  
You may need to override CMSSW's version of scikit learn in order to evaluate the BDT.  
To do so:  
```
cd CMSSW_X_X_X
cmsenv                                             # this is meant to have CMSSW's python version handy
cd                                                 # go back to your home
python -m pip install --upgrade --user sklearn     # do a local installation of the most recent scikit learn *against the correct python version!!*
```  

Now you only have to import the correct scikit learn module:
* modules are imported ordered as they appear in `sys.path`
* put the path to your local installation *first*, that is `sys.path.insert(0, os.environ['HOME'] + '/.local/lib/python2.7/site-packages')` 
