import PhysicsTools.HeppyCore.framework.config as cfg, os
from CMGTools.RootTools.samples.ComponentCreator import ComponentCreator
 
json   = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions17/13TeV/ReReco/Cert_294927-306462_13TeV_EOY2017ReReco_Collisions17_JSON_v1.txt'
jsonUL = '/gwpool/users/lguzzi/CMSSW_10_4_0/src/CMGTools/WTau3Mu/data/golden_jsons/Cert_294927-306462_13TeV_UL2017_Collisions17_GoldenJSON.txt'

kreator = ComponentCreator()

DoubleMuonLowMass_Run2017B_31Mar2018 = kreator.makeDataComponent('DoubleMuonLowMass_Run2017B_31Mar2018', '/DoubleMuonLowMass/Run2017B-31Mar2018-v1/MINIAOD', 'CMS', '.*root', json, useAAA=True)
DoubleMuonLowMass_Run2017C_31Mar2018 = kreator.makeDataComponent('DoubleMuonLowMass_Run2017C_31Mar2018', '/DoubleMuonLowMass/Run2017C-31Mar2018-v1/MINIAOD', 'CMS', '.*root', json, useAAA=True)
DoubleMuonLowMass_Run2017D_31Mar2018 = kreator.makeDataComponent('DoubleMuonLowMass_Run2017D_31Mar2018', '/DoubleMuonLowMass/Run2017D-31Mar2018-v1/MINIAOD', 'CMS', '.*root', json, useAAA=True)
DoubleMuonLowMass_Run2017E_31Mar2018 = kreator.makeDataComponent('DoubleMuonLowMass_Run2017E_31Mar2018', '/DoubleMuonLowMass/Run2017E-31Mar2018-v1/MINIAOD', 'CMS', '.*root', json, useAAA=True)
DoubleMuonLowMass_Run2017F_31Mar2018 = kreator.makeDataComponent('DoubleMuonLowMass_Run2017F_31Mar2018', '/DoubleMuonLowMass/Run2017F-31Mar2018-v1/MINIAOD', 'CMS', '.*root', json, useAAA=True)

datasamplesDoubleMuLowMass31Mar2018 = [
#    DoubleMuonLowMass_Run2017B_31Mar2018,
    DoubleMuonLowMass_Run2017C_31Mar2018,
    DoubleMuonLowMass_Run2017D_31Mar2018,
    DoubleMuonLowMass_Run2017E_31Mar2018,
    DoubleMuonLowMass_Run2017F_31Mar2018
]

DoubleMuonLowMass_Run2017B_09Aug2019_UL2017 = kreator.makeDataComponent('DoubleMuonLowMass_Run2017B_09Aug2019_UL2017', '/DoubleMuonLowMass/Run2017B-09Aug2019_UL2017-v1/MINIAOD', 'CMS', '.*root', jsonUL, useAAA=True)
DoubleMuonLowMass_Run2017C_09Aug2019_UL2017 = kreator.makeDataComponent('DoubleMuonLowMass_Run2017C_09Aug2019_UL2017', '/DoubleMuonLowMass/Run2017C-09Aug2019_UL2017-v1/MINIAOD', 'CMS', '.*root', jsonUL, useAAA=True)
DoubleMuonLowMass_Run2017D_09Aug2019_UL2017 = kreator.makeDataComponent('DoubleMuonLowMass_Run2017D_09Aug2019_UL2017', '/DoubleMuonLowMass/Run2017D-09Aug2019_UL2017-v1/MINIAOD', 'CMS', '.*root', jsonUL, useAAA=True)
DoubleMuonLowMass_Run2017E_09Aug2019_UL2017 = kreator.makeDataComponent('DoubleMuonLowMass_Run2017E_09Aug2019_UL2017', '/DoubleMuonLowMass/Run2017E-09Aug2019_UL2017-v1/MINIAOD', 'CMS', '.*root', jsonUL, useAAA=True)
DoubleMuonLowMass_Run2017F_09Aug2019_UL2017 = kreator.makeDataComponent('DoubleMuonLowMass_Run2017F_09Aug2019_UL2017', '/DoubleMuonLowMass/Run2017F-09Aug2019_UL2017-v1/MINIAOD', 'CMS', '.*root', jsonUL, useAAA=True)

datasamplesDoubleMuLowMass09Aug2019UL = [
    DoubleMuonLowMass_Run2017B_09Aug2019_UL2017,
    DoubleMuonLowMass_Run2017C_09Aug2019_UL2017,
    DoubleMuonLowMass_Run2017D_09Aug2019_UL2017,
    DoubleMuonLowMass_Run2017E_09Aug2019_UL2017,
    DoubleMuonLowMass_Run2017F_09Aug2019_UL2017,
]