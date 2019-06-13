import PhysicsTools.HeppyCore.framework.config as cfg
import os
import glob

#####COMPONENT CREATOR

from CMGTools.RootTools.samples.ComponentCreator import ComponentCreator
kreator = ComponentCreator()

## Pythia MC
bad_files = [
    '/gwteras/cms/store/user/lguzzi/WToTauNu_Tau3Mu_Pythia/CRAB3_MC_generation_300k_miniaod_smallfiles/190313_143423/0003/WTau3Mu-RunIIFall17_MINIAODSIM_3314.root',
]

files_2017_300k = glob.glob('/gwteras/cms/store/user/lguzzi/WToTauNu_Tau3Mu_Pythia/CRAB3_MC_generation_300k_miniaod_smallfiles/190313_143423/*/*.root')
files_2017_300k = [ff for ff in files_2017_300k if not ff in bad_files]

# first private production
WToTauTo3Mu = cfg.MCComponent(
    dataset       = 'WToTauTo3Mu',
    name          = 'WToTauTo3Mu',
    files         = files_2017_300k ,
    xSection      = 21490.9, # this uses the correct tau BR from the PDG # 20508.9 * 1.e-7, # W to lep nu / 3.[pb] x BR
#     xSection      = 20508.9 * 0.005, # W to lep nu / 3.[pb] x BR
    nGenEvents    = 342200,
    triggers      = ['HLT_Tau3Mu_Mu7_Mu1_TkMu1_IsoTau15_v%d' %i for i in range(1, 12)] + 
                    ['HLT_DoubleMu3_Trk_Tau3mu_v%d'          %i for i in range(1, 12)],
    effCorrFactor = 1,
)