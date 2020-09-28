import PhysicsTools.HeppyCore.framework.config as cfg
import os
import glob

#####COMPONENT CREATOR

from CMGTools.RootTools.samples.ComponentCreator import ComponentCreator
kreator = ComponentCreator()

WToTauTo3Mu_Pythia_taumass1p65 = cfg.MCComponent(
    dataset       = 'WToTauTo3Mu_1p65',
    name          = 'WToTauTo3Mu_1p65',
    files           = '/gwpool/users/lguzzi/Tau3Mu/2017_2018/MC_prod/MINIAODSIM/2018/wtotaunu_tau3mu_phytia_RunIIAutumn18MiniAOD_tauMass1p65.root',
    xSection      = 21490.9,
    nGenEvents    = 50000,
    effCorrFactor = 1,
)
WToTauTo3Mu_Pythia_taumass1p70 = cfg.MCComponent(
    dataset       = 'WToTauTo3Mu_1p70',
    name          = 'WToTauTo3Mu_1p70',
    files         = '/gwpool/users/lguzzi/Tau3Mu/2017_2018/MC_prod/MINIAODSIM/2018/wtotaunu_tau3mu_phytia_RunIIAutumn18MiniAOD_tauMass1p70.root',
    xSection      = 21490.9,
    nGenEvents    = 50000,
    effCorrFactor = 1,
)
WToTauTo3Mu_Pythia_taumass1p85 = cfg.MCComponent(
    dataset       = 'WToTauTo3Mu_1p85',
    name          = 'WToTauTo3Mu_1p85',
    files         = '/gwpool/users/lguzzi/Tau3Mu/2017_2018/MC_prod/MINIAODSIM/2018/wtotaunu_tau3mu_phytia_RunIIAutumn18MiniAOD_tauMass1p85.root',
    xSection      = 21490.9,
    nGenEvents    = 50000,
    effCorrFactor = 1,
)
WToTauTo3Mu_Pythia_taumass1p90 = cfg.MCComponent(
    dataset       = 'WToTauTo3Mu_1p90',
    name          = 'WToTauTo3Mu_1p90',
    files         = '/gwpool/users/lguzzi/Tau3Mu/2017_2018/MC_prod/MINIAODSIM/2018/wtotaunu_tau3mu_phytia_RunIIAutumn18MiniAOD_tauMass1p90.root',
    xSection      = 21490.9,
    nGenEvents    = 50000,
    effCorrFactor = 1,
)
WToTauTo3Mu_Pythia_taumass1p95 = cfg.MCComponent(
    dataset       = 'WToTauTo3Mu_1p95',
    name          = 'WToTauTo3Mu_1p95',
    files         = '/gwpool/users/lguzzi/Tau3Mu/2017_2018/MC_prod/MINIAODSIM/2018/wtotaunu_tau3mu_phytia_RunIIAutumn18MiniAOD_tauMass1p95.root',
    xSection      = 21490.9,
    nGenEvents    = 50000,
    effCorrFactor = 1,
)

WToTauTo3Mu_Pythia_shiftedMasses = [
    WToTauTo3Mu_Pythia_taumass1p65,
    WToTauTo3Mu_Pythia_taumass1p70,
    WToTauTo3Mu_Pythia_taumass1p85,
    WToTauTo3Mu_Pythia_taumass1p90,
    WToTauTo3Mu_Pythia_taumass1p95,
]

WToTauTo3Mu_PythiaUL_taumass1p95 = kreator.makeMCComponent(
    name    = 'WToTauTo3Mu_1p95',
    dataset = '/W_ToTau_ToMuMuMu_MTau1950_TuneCP5_13TeV-pythia8/RunIISummer19UL18MiniAOD-106X_upgrade2018_realistic_v11_L1v1-v2/MINIAODSIM',
    user    = 'CMS',
    pattern = '.*root',
    useAAA  = True,
)

WToTauTo3Mu_PythiaUL_taumass1p90 = kreator.makeMCComponent(
    name    = 'WToTauTo3Mu_1p90',
    dataset = '/W_ToTau_ToMuMuMu_MTau1900_TuneCP5_13TeV-pythia8/RunIISummer19UL18MiniAOD-106X_upgrade2018_realistic_v11_L1v1-v2/MINIAODSIM',
    user    = 'CMS',
    pattern = '.*root',
    useAAA  = True,
)

WToTauTo3Mu_PythiaUL_taumass1p85 = kreator.makeMCComponent(
    name    = 'WToTauTo3Mu_1p85',
    dataset = '/W_ToTau_ToMuMuMu_MTau1850_TuneCP5_13TeV-pythia8/RunIISummer19UL18MiniAOD-106X_upgrade2018_realistic_v11_L1v1-v2/MINIAODSIM',
    user    = 'CMS',
    pattern = '.*root',
    useAAA  = True,
)

WToTauTo3Mu_PythiaUL_taumass1p70 = kreator.makeMCComponent(
    name    = 'WToTauTo3Mu_1p70',
    dataset = '/W_ToTau_ToMuMuMu_MTau1700_TuneCP5_13TeV-pythia8/RunIISummer19UL18MiniAOD-106X_upgrade2018_realistic_v11_L1v1-v2/MINIAODSIM',
    user    = 'CMS',
    pattern = '.*root',
    useAAA  = True,
)

WToTauTo3Mu_PythiaUL_taumass1p65 = kreator.makeMCComponent(
    name    = 'WToTauTo3Mu_1p65',
    dataset = '/W_ToTau_ToMuMuMu_MTau1650_TuneCP5_13TeV-pythia8/RunIISummer19UL18MiniAOD-106X_upgrade2018_realistic_v11_L1v1-v2/MINIAODSIM',
    user    = 'CMS',
    pattern = '.*root',
    useAAA  = True,
)

WToTauTo3Mu_Pythia_UltraLegacy_shiftedMasses = [ 
    WToTauTo3Mu_PythiaUL_taumass1p95,
    WToTauTo3Mu_PythiaUL_taumass1p90,
    WToTauTo3Mu_PythiaUL_taumass1p85,
    WToTauTo3Mu_PythiaUL_taumass1p70,
    WToTauTo3Mu_PythiaUL_taumass1p65,
]