# Unofficial hotfix for CMGTools and Heppy
## [CMGTools] jec files
```
cd CMSSW_X_X_X/src/CMGTools
cmsenv
git remote add lca	https://github.com/lguzzi/cmgtools-lite
git fetch lca
git checkout -b myBranch_tau3mu # create a new branch just in case
git cherry-pick d5d12b7067ca5d5c05bc347570113c78605e5672
```
## [CMGTools] jet ID update
```
cd CMSSW_X_X_X/src/CMGTools
cmsenv
git remote add lca	https://github.com/lguzzi/cmgtools-lite
git fetch lca
git checkout -b myBranch_tau3mu # create a new branch just in case
git cherry-pick 82b6874b1d0f6f4407517e7a6a9380549eaa3e04
```

## [Heppy] trigger object slicing bugfix (rollback)
```
cd CMSSW_X_X_X/src
cmsenv
git remote add lca lca	https://github.com/lguzzi/cmg-cmssw
git fetch lca
git checkout -b heppy_myBranch_tau3mu # create a new branch just in case
git cherry-pick f3c07f0bb55858a7497e0ff1205bda2261d4e145
```

## [Heppy] add MIB to the batch manager and fix an unicode cast bug 
```
cd CMSSW_X_X_X/src
cmsenv
git remote add lca lca	https://github.com/lguzzi/cmg-cmssw
git fetch lca
git checkout -b heppy_myBranch_tau3mu # create a new branch just in case
git cherry-pick 3c521d4bcd001d5e9b6725a94b20d8304d1d2a54
git cherry-pick 5e2793d9bb7057f82d421cc8a432914980d65195
```

## [Heppy] fix bug in Tau class relIso function oveloading
```
cd CMSSW_X_X_X/src
cmsenv
git remote add lca lca	https://github.com/lguzzi/cmg-cmssw
git fetch lca
git checkout -b heppy_myBranch_tau3mu # create a new branch just in case
git cherry-pick 1febfc9d05561716a78ba044e2c6ad4535add061
```
