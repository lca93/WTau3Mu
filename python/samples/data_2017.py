import PhysicsTools.HeppyCore.framework.config as cfg, os
from CMGTools.RootTools.samples.ComponentCreator import ComponentCreator
 
json = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions17/13TeV/ReReco/Cert_294927-306462_13TeV_EOY2017ReReco_Collisions17_JSON_v1.txt'

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