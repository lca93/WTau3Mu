import PhysicsTools.HeppyCore.framework.config as cfg, os
from CMGTools.RootTools.samples.ComponentCreator import ComponentCreator
 
json = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions18/13TeV/PromptReco/Cert_314472-325175_13TeV_PromptReco_Collisions18_JSON.txt'

kreator = ComponentCreator()


#DoubleMuonLowMass_Run2018A_17Sep2018 = kreator.makeDataComponent('DoubleMuonLowMass_Run2018A_17Sep2018', '/DoubleMuonLowMass/Run2018A-17Sep2018-v1/MINIAOD', 'CMS', '.*root', json, useAAA=True)
#DoubleMuonLowMass_Run2018B_17Sep2018 = kreator.makeDataComponent('DoubleMuonLowMass_Run2018B_17Sep2018', '/DoubleMuonLowMass/Run2018B-17Sep2018-v1/MINIAOD', 'CMS', '.*root', json, useAAA=True)
#DoubleMuonLowMass_Run2018C_17Sep2018 = kreator.makeDataComponent('DoubleMuonLowMass_Run2018C_17Sep2018', '/DoubleMuonLowMass/Run2018C-17Sep2018-v1/MINIAOD', 'CMS', '.*root', json, useAAA=True)

DoubleMuonLowMass_Run2018A_PromptReco = kreator.makeDataComponent('DoubleMuonLowMass_Run2018A_PromptReco', '/DoubleMuonLowMass/Run2018A-PromptReco-v3/MINIAOD', 'CMS', '.*root', json, useAAA=True)
DoubleMuonLowMass_Run2018B_PromptReco = kreator.makeDataComponent('DoubleMuonLowMass_Run2018B_PromptReco', '/DoubleMuonLowMass/Run2018B-PromptReco-v2/MINIAOD', 'CMS', '.*root', json, useAAA=True)
DoubleMuonLowMass_Run2018C_PromptReco = kreator.makeDataComponent('DoubleMuonLowMass_Run2018C_PromptReco', '/DoubleMuonLowMass/Run2018C-PromptReco-v3/MINIAOD', 'CMS', '.*root', json, useAAA=True)
DoubleMuonLowMass_Run2018D_PromptReco = kreator.makeDataComponent('DoubleMuonLowMass_Run2018D_PromptReco', '/DoubleMuonLowMass/Run2018D-PromptReco-v2/MINIAOD', 'CMS', '.*root', json, useAAA=True)

datasamplesDoubleMuLowMass_17Sep2018 = [
#datasamplesDoubleMuLowMass_PromptReco = [
    #DoubleMuonLowMass_Run2018A_17Sep2018,
    DoubleMuonLowMass_Run2018A_PromptReco,
    #DoubleMuonLowMass_Run2018B_17Sep2018,
    DoubleMuonLowMass_Run2018B_PromptReco,
    #DoubleMuonLowMass_Run2018C_17Sep2018,
    DoubleMuonLowMass_Run2018C_PromptReco,
    DoubleMuonLowMass_Run2018D_PromptReco,
]