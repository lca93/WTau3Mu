#Unofficial hotfix for CMGTools and Heppy
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
git cherry-pick 1f60ad104285682c04452a1b13e8dae4456f0e49
```

## [Heppy] add MIB to the batch manager and fix an unicode cast bug 
```
cd CMSSW_X_X_X/src
cmsenv
git remote add lca lca	https://github.com/lguzzi/cmg-cmssw
git fetch lca
git checkout -b heppy_myBranch_tau3mu # create a new branch just in case
git cherry-pick b603b53964c96fa3a0bc198f4fd05b2ec80432c9
git cherry-pick f42dabed7cf4398d014e54382dc3398661a06e11
git cherry-pick d0d64ee4f43e8e6985681b0c5650053469c82013
```


