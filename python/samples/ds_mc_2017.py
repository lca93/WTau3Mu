import PhysicsTools.HeppyCore.framework.config as cfg
import os

from CMGTools.RootTools.samples.ComponentCreator import ComponentCreator

creator = ComponentCreator()

DsTau3Mu = creator.makeMCComponent(
    name        = 'DsPhiMuMuPi' ,
    dataset     = '/DsToTau_To3Mu_MuFilter_TuneCUEP8M1_13TeV-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',
    user        = 'CMS'         , 
    pattern     = '.*root'      ,
    useAAA      = True          ,
)

DsTau3Mu.nGenEvents  = 3665609