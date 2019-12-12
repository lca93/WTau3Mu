# Unofficial hotfix for CMGTools and Heppy
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
