import PhysicsTools.HeppyCore.framework.config as cfg
import os
import glob

#####COMPONENT CREATOR

from CMGTools.RootTools.samples.ComponentCreator import ComponentCreator
kreator = ComponentCreator()

## Pt-20ToInfw
QCD_Pt20toInf_MuEnrichedPt15 = kreator.makeMCComponent(
    name        = 'QCD_Pt-20toInf_MuEnrichedPt15' ,
    dataset     = '/QCD_Pt-20toInf_MuEnrichedPt15_TuneCP5_13TeV_pythia8/RunIISpring18MiniAOD-100X_upgrade2018_realistic_v10-v1/MINIAODSIM',
    user        = 'CMS'         , 
    pattern     = '.*root'      ,
    useAAA      = True          ,
)
QCD_Pt20toInf_MuEnrichedPt15.nGenEvents  = 22291129

## Pt-15to20

## GEN-SIM /QCD_Pt-15to20_MuEnrichedPt5_TuneCP5_13TeV_pythia8/RunIIFall18GS-102X_upgrade2018_realistic_v11_ext1-v1/GEN-SIM
QCD_Pt_15to20_MuEnrichedPt5 = kreator.makeMCComponent(
    name        = 'QCD_Pt-15to20_MuEnrichedPt5' ,
    dataset     = '/QCD_Pt-15to20_MuEnrichedPt5_TuneCP5_13TeV_pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v3/MINIAODSIM',
    user        = 'CMS'         , 
    pattern     = '.*root'      ,
    useAAA      = True          ,
)
QCD_Pt_15to20_MuEnrichedPt5.nGenEvents  = 4576065

QCD_MuEnriched = [QCD_Pt_15to20_MuEnrichedPt5, QCD_Pt20toInf_MuEnrichedPt15]
