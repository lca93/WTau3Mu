import PhysicsTools.HeppyCore.framework.config as cfg
import os
import glob

#####COMPONENT CREATOR

from CMGTools.RootTools.samples.ComponentCreator import ComponentCreator
kreator = ComponentCreator()

//Pythia MC
WToTauTo3Mu = kreator.makePrivateMCComponent(
    name       = 'WToTauTo3Mu',
    dataset    = '/WToTauNu_Tau3Mu_Pythia/lguzzi-CRAB3_MC_generation_40k_miniaod_smallfiles-5f646ecd4e1c7a39ab0ed099ff55ceb9/USER',
    prefix = 'root://cms-xrd-global.cern.ch',
    xSec       = 20508.9 * 1.e-7, # W to lep nu / 3.[pb] x BR
)
WToTauTo3Mu.files = glob.glob('/eos/user/l/lguzzi/WTau3Mu/samples/2017/MC/*.root')

//MadGraph MC
WToTauTo3Mu_MG = kreator.makeMCComponent(
    name       = 'WToTauTo3Mu',
    dataset    = '/WToTauNu_TauTo3Mu_MadGraph_13TeV/PhaseIFall16MiniAOD-FlatPU28to62HcalNZSRAW_PhaseIFall16_90X_upgrade2017_realistic_v6_C1-v1/MINIAODSIM',
    user       = 'CMS',
    pattern    = '.*root',
    xSec       = 20508.9 * 1.e-7, # W to lep nu / 3.[pb] x BR
    useAAA     = True,
)

