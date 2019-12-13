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
git cherry-pick 97329e41eb333394a3a15956d67f3cea67427260 		## add the batch script and the HTCondor support 
git cherry-pick 2bbce12038206ece2302a9513babd5a0acaaf949		## fix proxy env. variable issue
cd $CMSSW_BASE/bin/$SCRAM_ARCH
mv heppy_batch.py heppy_batch.py.old
ln -s $CMSSW_BASE/src/PhysicsTools/HeppyCore/scripts/heppy_batch.py .
mv run_condor_simple.sh run_condor_simple.sh.old
ln -s $CMSSW_BASE/src/PhysicsTools/HeppyCore/scripts/run_condor_simple.sh .
```

