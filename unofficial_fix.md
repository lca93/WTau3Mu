# Outdated
#

# Unofficial fix for Heppy (release 94X)
## [Heppy] trigger object slicing bugfix (rollback)
```
cd CMSSW_X_X_X/src
cmsenv
git remote add lca https://github.com/lguzzi/cmg-cmssw
git fetch lca
git checkout -b heppy_94X_tau3mu
git cherry-pick 53fe924f6012d01284e48e7fd083f0a7c99a1f63
```

## [Heppy] disable completely the looper print out
```
cd CMSSW_X_X_X/src
cmsenv
git remote add lca https://github.com/lguzzi/cmg-cmssw
git fetch lca
git checkout -b heppy_94X_tau3mu
git cherry-pick a09c1e80387fb9f029105f07f7cc9d9a33c1b92e
```

## [Heppy] add MIB to the batch manager 
```
cd CMSSW_X_X_X/src
cmsenv
git remote add lca https://github.com/lguzzi/cmg-cmssw
git fetch lca
git checkout -b heppy_94X_tau3mu
git cherry-pick 97329e41eb333394a3a15956d67f3cea67427260 		## add the batch script and the HTCondor support 
git cherry-pick 2bbce12038206ece2302a9513babd5a0acaaf949		## fix proxy env. variable issue
cd $CMSSW_BASE/bin/$SCRAM_ARCH
mv heppy_batch.py heppy_batch.py.old
ln -s $CMSSW_BASE/src/PhysicsTools/HeppyCore/scripts/heppy_batch.py .
mv run_condor_simple.sh run_condor_simple.sh.old
ln -s $CMSSW_BASE/src/PhysicsTools/HeppyCore/scripts/run_condor_simple.sh .
```

# Unofficial fix for Heppy (release 102X)
## [Heppy] trigger object slicing bugfix (rollback)
```
cd CMSSW_X_X_X/src
cmsenv
git remote add lca https://github.com/lguzzi/cmg-cmssw
git fetch lca
git checkout -b heppy_102X_tau3mu
git cherry-pick cdc5748e7c03d0e4e3ac5c91215b6cbb6b2b6d81
```

## [Heppy] disable completely the looper print out
```
cd CMSSW_X_X_X/src
cmsenv
git remote add lca https://github.com/lguzzi/cmg-cmssw
git fetch lca
git checkout -b heppy_102X_tau3mu
git cherry-pick 1672f937f835c3418ce2d41dcac19719ba9f64de
```

## [Heppy] add MIB to the batch manager 
```
cd CMSSW_X_X_X/src
cmsenv
git remote add lca https://github.com/lguzzi/cmg-cmssw
git fetch lca
git checkout -b heppy_102X_tau3mu
git cherry-pick 6443c9cdcb9da61fee2e523d5715d5ac6e0c9b7c 		## add the batch script and the HTCondor support 
git cherry-pick b794a0a6c8b35ddc13fcdfccad27f8586d24e1a6		## fix proxy env. variable issue
cd $CMSSW_BASE/bin/$SCRAM_ARCH
mv heppy_batch.py heppy_batch.py.old
ln -s $CMSSW_BASE/src/PhysicsTools/HeppyCore/scripts/heppy_batch.py .
mv run_condor_simple.sh run_condor_simple.sh.old
ln -s $CMSSW_BASE/src/PhysicsTools/HeppyCore/scripts/run_condor_simple.sh .
```



