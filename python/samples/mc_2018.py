import PhysicsTools.HeppyCore.framework.config as cfg
import os
import glob

#####COMPONENT CREATOR

from CMGTools.RootTools.samples.ComponentCreator import ComponentCreator
kreator = ComponentCreator()

## Pythia MC
bad_files = [
]

files_2018_400k = glob.glob('/gwteras/cms/store/user/lguzzi/WToTauNu_Tau3Mu_Pythia/CRAB3_MC_generation_400k_miniaod_smallfiles/190321_150932/*/*.root')
files_2018_400k = [ff for ff in files_2018_400k if not ff in bad_files]

# first private production
WToTauTo3Mu_Pythia = cfg.MCComponent(
    dataset       = 'WToTauTo3Mu',
    name          = 'WToTauTo3Mu',
    files         = files_2018_400k ,
    xSection      = 21490.9, # this uses the correct tau BR from the PDG # 20508.9 * 1.e-7, # W to lep nu / 3.[pb] x BR
#     xSection      = 20508.9 * 0.005, # W to lep nu / 3.[pb] x BR
    nGenEvents    = 342200,
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

WToTauTo3Mu_Pythia_taumass1p65 = cfg.MCComponent(
    dataset       = 'WToTauTo3Mu',
    name          = 'WToTauTo3Mu',
    files         = '/gwpool/users/lguzzi/Tau3Mu/2017_2018/MC_prod/mc_2017/different_mass/miniaod/WTau3Mu-RunIIFall17_MINIAODSIM.root' ,
    xSection      = 21490.9, # this uses the correct tau BR from the PDG # 20508.9 * 1.e-7, # W to lep nu / 3.[pb] x BR
#     xSection      = 20508.9 * 0.005, # W to lep nu / 3.[pb] x BR
    nGenEvents    = 100,
    effCorrFactor = 1,
)
