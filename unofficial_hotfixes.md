# Unofficial hotfix for Heppy (release 94X)
## [Heppy] trigger object slicing bugfix (rollback)
```
cd CMSSW_X_X_X/src
cmsenv
git remote add lca https://github.com/lguzzi/cmg-cmssw
git fetch lca
git checkout -b heppy_94X_tau3mu # create a new branch just in case
git cherry-pick 53fe924f6012d01284e48e7fd083f0a7c99a1f63
```

## [Heppy] add MIB to the batch manager 
```
cd CMSSW_X_X_X/src
cmsenv
git remote add lca https://github.com/lguzzi/cmg-cmssw
git fetch lca
git checkout -b heppy_94X_tau3mu # create a new branch just in case
git cherry-pick 071f3015237a3c2bfca07bff528fd562f08b127c
```
