
# import dill # needed in order to serialise lambda functions, need to be installed by the user. See http://stackoverflow.com/questions/25348532/can-python-pickle-lambda-functions
from collections import OrderedDict, Counter
import os
import PhysicsTools.HeppyCore.framework.config as cfg
from PhysicsTools.HeppyCore.framework.config     import printComps
from PhysicsTools.HeppyCore.framework.heppy_loop import getHeppyOption
from PhysicsTools.Heppy.utils.cmsswPreprocessor  import CmsswPreprocessor
from CMGTools.RootTools.utils.splitFactor        import splitFactor

# import all analysers:
# Heppy analyzers
from PhysicsTools.Heppy.analyzers.core.JSONAnalyzer                 import JSONAnalyzer
from PhysicsTools.Heppy.analyzers.core.SkimAnalyzerCount            import SkimAnalyzerCount
from PhysicsTools.Heppy.analyzers.core.EventSelector                import EventSelector
from PhysicsTools.Heppy.analyzers.objects.VertexAnalyzer            import VertexAnalyzer
from PhysicsTools.Heppy.analyzers.core.PileUpAnalyzer               import PileUpAnalyzer
from PhysicsTools.Heppy.analyzers.gen.GeneratorAnalyzer             import GeneratorAnalyzer
from PhysicsTools.Heppy.analyzers.gen.LHEWeightAnalyzer             import LHEWeightAnalyzer
        
# Tau-tau analysers        
from CMGTools.H2TauTau.proto.analyzers.METFilter                    import METFilter
from CMGTools.H2TauTau.proto.analyzers.FileCleaner                  import FileCleaner

#WTau3Mu analysers
from CMGTools.WTau3Mu.analyzers.JetAnalyzer                         import JetAnalyzer
from CMGTools.WTau3Mu.analyzers.TriggerAnalyzer                     import TriggerAnalyzer
from CMGTools.WTau3Mu.analyzers.Tau3MuAnalyzer                      import Tau3MuAnalyzer
from CMGTools.WTau3Mu.analyzers.WTau3MuTreeProducer                 import WTau3MuTreeProducer
from CMGTools.WTau3Mu.analyzers.Tau3MuKalmanVertexFitterAnalyzer    import Tau3MuKalmanVertexFitterAnalyzer
from CMGTools.WTau3Mu.analyzers.Tau3MuKinematicVertexFitterAnalyzer import Tau3MuKinematicVertexFitterAnalyzer
from CMGTools.WTau3Mu.analyzers.Tau3MuIsolationAnalyzer             import Tau3MuIsolationAnalyzer
from CMGTools.WTau3Mu.analyzers.GenMatcherAnalyzer                  import GenMatcherAnalyzer
from CMGTools.WTau3Mu.analyzers.L1TriggerAnalyzer                   import L1TriggerAnalyzer
from CMGTools.WTau3Mu.analyzers.BDTAnalyzer                         import BDTAnalyzer
from CMGTools.WTau3Mu.analyzers.MVAMuonIDAnalyzer                   import MVAMuonIDAnalyzer
from CMGTools.WTau3Mu.analyzers.RecoilCorrector                     import RecoilCorrector

# import samples
from CMGTools.WTau3Mu.samples.data_2018                             import datasamplesDoubleMuLowMass_PromptReco as samples

puFileData = '{CMS}/src/CMGTools/WTau3Mu/data/pileup/Data_PileUp_2018_69p2.root'     .format(CMS = os.path.expandvars('$CMSSW_BASE'))
puFileMC   = '{CMS}/src/CMGTools/WTau3Mu/data/pileup/MC_PU_2018_miniAOD_WTau3Mu.root'.format(CMS = os.path.expandvars('$CMSSW_BASE'))

###################################################
###                   OPTIONS                   ###
###################################################
# Get all heppy options; set via "-o production" or "-o production=True"
# production = True run on batch, production = False (or unset) run locally
production         = getHeppyOption('production'        , True )
pick_events        = getHeppyOption('pick_events'       , False)
kin_vtx_fitter     = getHeppyOption('kin_vtx_fitter'    , True )
extrap_muons_to_L1 = getHeppyOption('extrap_muons_to_L1', False)
compute_mvamet     = getHeppyOption('compute_mvamet'    , False)
use_mvamet         = getHeppyOption('use_mvamet'        , False)
use_puppimet       = getHeppyOption('use_puppimet'      , True )

if use_mvamet and use_puppimet:
    print 'WARNING: ignoring PUPPI MET, using MVA MET'
    use_puppimet = False

###################################################
###               HANDLE SAMPLES                ###
###################################################
for sample in samples:
    # triggers you want in DoubleMuonLowMass
    sample.triggers    = ['HLT_Tau3Mu_Mu7_Mu1_TkMu1_IsoTau15_v%d'         %i for i in range(1, 12)]
    sample.triggers   += ['HLT_Tau3Mu_Mu5_Mu1_TkMu1_IsoTau10_Charge1_v%d' %i for i in range(1, 12)]
    sample.triggers   += ['HLT_DoubleMu3_Trk_Tau3mu_v%d'                  %i for i in range(1, 12)]

    sample.splitFactor = splitFactor(sample, 3e05)
    sample.puFileData  = puFileData
    sample.puFileMC    = puFileMC
    
selectedComponents = samples

###################################################
###                  ANALYSERS                  ###
###################################################
eventSelector = cfg.Analyzer(
    EventSelector,
    name='EventSelector',
    toSelect=[
        588661057,
    ]
)

lheWeightAna = cfg.Analyzer(
    LHEWeightAnalyzer, name="LHEWeightAnalyzer",
    useLumiInfo=False
)

jsonAna = cfg.Analyzer(
    JSONAnalyzer,
    name='JSONAnalyzer',
)

skimAna = cfg.Analyzer(
    SkimAnalyzerCount,
    name='SkimAnalyzerCount'
)

triggerAna = cfg.Analyzer(
    TriggerAnalyzer,
    name='TriggerAnalyzer',
    addTriggerObjects=True,
    requireTrigger=True,
    usePrescaled=False,
    unpackLabels=True,
    triggerObjectsHandle = ['slimmedPatTrigger', '', 'RECO'],
)

vertexAna = cfg.Analyzer(
    VertexAnalyzer,
    name='VertexAnalyzer',
    fixedWeight=1,
    keepFailingEvents=True,
    verbose=False
)

pileUpAna = cfg.Analyzer(
    PileUpAnalyzer,
    name='PileUpAnalyzer',
    true=True
)

# for each path specify which filters you want the muons to match to
triggers_and_filters = OrderedDict()

## trigger matching to be implemented in Tau3MuAnalyzer for 2017 trigger
# triggers_and_filters['HLT_Tau3Mu_Mu7_Mu1_TkMu1_IsoTau15'] = (['hltTau3MuIsoFilter', 'hltTau3MuIsoFilter', 'hltTau3MuIsoFilter'], Counter({83:2, 91:1}))  
triggers_and_filters['HLT_Tau3Mu_Mu7_Mu1_TkMu1_IsoTau15']           = (['hltTau3MuPreFilter'       ], Counter({84:1})) ## is it 84?
triggers_and_filters['HLT_Tau3Mu_Mu5_Mu1_TkMu1_IsoTau10_Charge1']   = (['hltTau3MuPreFilterCharge1'], Counter({84:1}))
triggers_and_filters['HLT_DoubleMu3_Trk_Tau3mu']                    = (['hltTau3muTkVertexFilter', 'hltTau3muTkVertexFilter', 'hltTau3muTkVertexFilter'], Counter({83:2, 91:1}))

tau3MuAna = cfg.Analyzer(
    Tau3MuAnalyzer,
    name='Tau3MuAnalyzer',
    trigger_match = triggers_and_filters,
    spectators  = ['HLT_DoubleMu3_Trk_Tau3mu'],
    useMVAmet   = use_mvamet  ,
    usePUPPImet = use_puppimet,
)

treeProducer = cfg.Analyzer(
    WTau3MuTreeProducer,
    name='WTau3MuTreeProducer',
    fillL1=False,
)

## see https://github.com/vinzenzstampf/HNL/blob/master/cfg/hnl_3l_reco_data_prompt_e_cfg.py#L118-L133
## twiki https://twiki.cern.ch/twiki/bin/viewauth/CMS/MissingETOptionalFiltersRun2#2017_data
metFilter = cfg.Analyzer(
    METFilter,
    name='METFilter',
    processName='RECO',
    triggers=[
        'Flag_goodVertices',
        'Flag_globalSuperTightHalo2016Filter',
        'Flag_HBHENoiseFilter',
        'Flag_HBHENoiseIsoFilter',
        'Flag_EcalDeadCellTriggerPrimitiveFilter',
        'Flag_BadPFMuonFilter',
        'Flag_BadChargedCandidateFilter',       ## marked as "not reccomended, under review" on the twiki
        'Flag_eeBadScFilter',
        'Flag_ecalBadCalibFilter',              ## NOTE: not listed on the twiki
        'ecalBadCalibReducedMINIAODFilter',     ## NOTE: to be rerun on miniaod?, see twiki
    ]
)

if kin_vtx_fitter:
    vertexFitter = cfg.Analyzer(
        Tau3MuKinematicVertexFitterAnalyzer,
        name='Tau3MuKinematicVertexFitterAnalyzer',
    )
else:
    vertexFitter = cfg.Analyzer(
        Tau3MuKalmanVertexFitterAnalyzer,
        name='Tau3MuKalmanVertexFitterAnalyzer',
    )
    

isoAna = cfg.Analyzer(
    Tau3MuIsolationAnalyzer,
    name='Tau3MuIsolationAnalyzer',
)

level1Ana = L1TriggerAnalyzer.defaultConfig
level1Ana.process = 'RECO'

bdtAna = cfg.Analyzer(
    BDTAnalyzer,
    name='BDTAnalyzer',
)

muIdAna = cfg.Analyzer(
    MVAMuonIDAnalyzer,
    name='MVAMuonIDAnalyzer',
    xml_pathBB = 'TMVA-muonid-bmm4-B-25.weights.xml',
    xml_pathEC = 'TMVA-muonid-bmm4-E-19.weights.xml',
    useBkgID = False,
    useSigID = True,
    useSideBands = False,
)

recoilAna = cfg.Analyzer(
    RecoilCorrector,
    name='RecoilCorrector',
    pfMetRCFile='CMGTools/WTau3Mu/data/recoilCorrections/TypeI-PFMet_Run2016BtoH.root',
)

# see SM HTT TWiki
# https://twiki.cern.ch/twiki/bin/viewauth/CMS/SMTauTau2016#Jet_Energy_Corrections
jetAna = cfg.Analyzer(
    JetAnalyzer,
    name              = 'JetAnalyzer',
    jetCol            = 'slimmedJets',
    jetPt             = 20.,
    jetEta            = 4.7,
    relaxJetId        = False, # relax = do not apply jet ID
    relaxPuJetId      = True,  # relax = do not apply pileup jet ID
    jerCorr           = False,
    puJetIDDisc       = 'pileupJetId:fullDiscriminant',
    recalibrateJets   = True,
    applyL2L3Residual = 'MC',
    mcGT              = '80X_mcRun2_asymptotic_2016_TrancheIV_v8',
    dataGT            = '80X_dataRun2_2016SeptRepro_v7',
    #jesCorr = 1., # Shift jet energy scale in terms of uncertainties (1 = +1 sigma)
)

fileCleaner = cfg.Analyzer(
    FileCleaner,
    name='FileCleaner'
)

###################################################
###                  SEQUENCE                   ###
###################################################
sequence = cfg.Sequence([
    lheWeightAna,
    jsonAna,
    skimAna,
    triggerAna, # First analyser that applies selections
    vertexAna,
    pileUpAna,
    tau3MuAna,
    jetAna,
    vertexFitter,
#    muIdAna,
    isoAna,
#    level1Ana,
    bdtAna,
    metFilter,
    treeProducer,
])

###################################################
###            SET BATCH OR LOCAL               ###
###################################################
if not production:
    comp                 = samples[0]
    selectedComponents   = [comp]
    comp.splitFactor     = 1
    comp.fineSplitFactor = 1
    comp.files = [
        'root://cms-xrd-global.cern.ch//store/data/Run2018A/DoubleMuonLowMass/MINIAOD/17Sep2018-v1/120000/378FEF34-8D97-B945-8F86-866FD8B945BF.root',
        'root://cms-xrd-global.cern.ch//store/data/Run2018A/DoubleMuonLowMass/MINIAOD/17Sep2018-v1/100000/303B5AAE-F4C3-6343-8C9A-876AB7E10127.root',
        'root://cms-xrd-global.cern.ch//store/data/Run2018A/DoubleMuonLowMass/MINIAOD/17Sep2018-v1/120000/0CA55195-A049-214E-B670-A4007E3E4B15.root',
        'root://cms-xrd-global.cern.ch//store/data/Run2018A/DoubleMuonLowMass/MINIAOD/17Sep2018-v1/120000/411ED742-6A55-5248-A1A5-D582254423C7.root',
        'root://cms-xrd-global.cern.ch//store/data/Run2018A/DoubleMuonLowMass/MINIAOD/17Sep2018-v1/120000/3D91DF68-E990-E44F-847D-6083E4078FCD.root',
        'root://cms-xrd-global.cern.ch//store/data/Run2018A/DoubleMuonLowMass/MINIAOD/17Sep2018-v1/120000/CFE6673D-C1AA-934C-BF9E-EB033BE19F2B.root',
        'root://cms-xrd-global.cern.ch//store/data/Run2018A/DoubleMuonLowMass/MINIAOD/17Sep2018-v1/120000/B6616C94-D54C-FF4B-912F-D75D09964B69.root',
        'root://cms-xrd-global.cern.ch//store/data/Run2018A/DoubleMuonLowMass/MINIAOD/17Sep2018-v1/270000/39CC35AB-1473-DA49-A4C9-5D7F255A33C0.root',
    ]

preprocessor = None

if extrap_muons_to_L1:
    fname = '$CMSSW_BASE/src/CMGTools/WTau3Mu/prod/muon_extrapolator_cfg.py'
    sequence.append(fileCleaner)
    preprocessor = CmsswPreprocessor(fname, addOrigAsSecondary=False)

if compute_mvamet:
    fname = '$CMSSW_BASE/src/CMGTools/WTau3Mu/prod/compute_mva_met_data_cfg.py'
    sequence.append(fileCleaner)
    preprocessor = CmsswPreprocessor(fname, addOrigAsSecondary=False)


# the following is declared in case this cfg is used in input to the
# heppy.py script
from PhysicsTools.HeppyCore.framework.eventsfwlite import Events
config = cfg.Config(
    components   = selectedComponents,
    sequence     = sequence,
    services     = [],
    preprocessor = preprocessor,
    events_class = Events
)

printComps(config.components, True)
