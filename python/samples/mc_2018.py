import PhysicsTools.HeppyCore.framework.config as cfg
import os
import glob

#####COMPONENT CREATOR

from CMGTools.RootTools.samples.ComponentCreator import ComponentCreator
kreator = ComponentCreator()

## Pythia MC
files_2018_400k = glob.glob('/gwteras/cms/store/user/lguzzi/WToTauNu_Tau3Mu_Pythia_RunIIFall18/crab_miniaod/200501_160511/0000/wtotaunu_tau3mu_phytia_RunIIAutumn18MiniAOD_*.root')
# first private production (BR bug)
#files_2018_400k = glob.glob('/gwteras/cms/store/user/lguzzi/WToTauNu_Tau3Mu_Pythia/CRAB3_MC_generation_400k_miniaod_smallfiles/190321_150932/*/*.root')

WToTauTo3Mu_Pythia = cfg.MCComponent(
    dataset       = 'WToTauTo3Mu',
    name          = 'WToTauTo3Mu',
    files         = files_2018_400k ,
    xSection      = 21490.9, # this uses the correct tau BR from the PDG # 20508.9 * 1.e-7, # W to lep nu / 3.[pb] x BR
    nGenEvents    = 381627,
    effCorrFactor = 1,
)


# use this one, larger stats!
WToTauTo3Mu_MadGraph = kreator.makeMCComponent(
    name        = 'WToTauTo3Mu' ,
    dataset     = '/W_ToTau_ToMuMuMu_TuneCP5_13TeV-pythia8-madgraph/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM',
    user        = 'CMS'         , 
    pattern     = '.*root'      ,
    useAAA      = True          ,
)

WToTauNu_Tau3Mu_Pythia_UL = cfg.MCComponent(
    dataset       = 'WToTauTo3Mu',
    name          = 'WToTauTo3Mu',
    files         = '/gwpool/users/lguzzi/Tau3Mu/2017_2018/MC_prod/ultralegacy/MINIAOD/WTau3Mu_BPH-RunIISummer19UL18MiniAOD-00008_v2.root',
    xSection      = 21490.9, # this uses the correct tau BR from the PDG # 20508.9 * 1.e-7, # W to lep nu / 3.[pb] x BR
    nGenEvents    = 50000,
    effCorrFactor = 1,
)

WToTauNu_Tau3Mu_Pythia_ULcentral = kreator.makeMCComponent(
    name        = 'WToTauTo3Mu' ,
    dataset     = '/W_ToTau_ToMuMuMu_TuneCP5_13TeV-pythia8/RunIISummer19UL18MiniAOD-106X_upgrade2018_realistic_v11_L1v1-v2/MINIAODSIM',
    user        = 'CMS'         ,
    pattern     = '.*root'      ,
    useAAA      = True          ,
)