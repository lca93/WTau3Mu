import ROOT
from CMGTools.WTau3Mu.analyzers.WTau3MuTreeProducerBase import WTau3MuTreeProducerBase
from PhysicsTools.HeppyCore.utils.deltar import deltaR
from itertools import product

global muon_mass
muon_mass = 0.1056583745

class WTau3MuTreeProducer(WTau3MuTreeProducerBase):

    '''
    '''

    def declareVariables(self, setup):
        '''
        '''
        self.bookEvent(self.tree)
        self.bookTriplet(self.tree, 'cand')
        self.bookTriplet(self.tree, 'cand_refit')
        self.bookMuon(self.tree, 'mu1')
        self.bookMuon(self.tree, 'mu2')
        self.bookMuon(self.tree, 'mu3')
        self.bookMuon(self.tree, 'mu1_refit')
        self.bookMuon(self.tree, 'mu2_refit')
        self.bookMuon(self.tree, 'mu3_refit')        
        self.bookVertex(self.tree, 'tau_sv')

        # jet information
        self.bookJet(self.tree, 'jet1' , fill_extra=False)
        self.bookJet(self.tree, 'jet2' , fill_extra=False)
        self.bookJet(self.tree, 'bjet1', fill_extra=False)
        self.bookJet(self.tree, 'bjet2', fill_extra=False)
        self.var(self.tree, 'HTjets' )
        self.var(self.tree, 'HTbjets')
        self.var(self.tree, 'njets'  )
        self.var(self.tree, 'nbjets' )
        self.var(self.tree, 'ncand_hltpass')
        self.var(self.tree, 'dR_tau_hlt')

        # generator information
        self.bookGenParticle(self.tree, 'gen_w')
        self.bookGenParticle(self.tree, 'mu1_gen')
        self.bookGenParticle(self.tree, 'mu2_gen')
        self.bookGenParticle(self.tree, 'mu3_gen')
        self.bookGenParticle(self.tree, 'cand_refit_gen')
        self.bookParticle(self.tree, 'gen_met')

        ## particles information
        self.bookParticle(self.tree, 'HLT_tau')

        ## MET filter information
        self.var(self.tree, 'Flag_goodVertices'                      , type=int, storageType='B'),
        self.var(self.tree, 'Flag_globalSuperTightHalo2016Filter'    , type=int, storageType='B'),
        self.var(self.tree, 'Flag_HBHENoiseFilter'                   , type=int, storageType='B'),
        self.var(self.tree, 'Flag_HBHENoiseIsoFilter'                , type=int, storageType='B'),
        self.var(self.tree, 'Flag_EcalDeadCellTriggerPrimitiveFilter', type=int, storageType='B'),
        self.var(self.tree, 'Flag_BadPFMuonFilter'                   , type=int, storageType='B'),
        self.var(self.tree, 'Flag_eeBadScFilter'                     , type=int, storageType='B'),
        self.var(self.tree, 'passBadMuonFilter'                      , type=int, storageType='B'),
        self.var(self.tree, 'passBadChargedHadronFilter'             , type=int, storageType='B'),

        #self.var(self.tree, 'Flag_BadChargedCandidateFilter'         , type=int, storageType='B'),
        #self.var(self.tree, 'Flag_ecalBadCalibFilter'                , type=int, storageType='B'),
        #self.var(self.tree, 'ecalBadCalibReducedMINIAODFilter'       , type=int, storageType='B'),

        ## Resonances (see PiKMassAnalyzer)
        self.list_of_mass_hypothesis = []
        ## build the mass hypothesis combinations accoridng to PiKMassAnalyzer definitions
        for ll in ( ('k', 'p'), ('k', 'm'), ('p', 'm')):
            for (l1, l2, l3) in product(ll, repeat = 3):
                if l1 == l2 == l3: continue
                ## only 0 or 2 muons
                if sum([obj == 'm' for obj in (l1, l2, l3)]) == 1:
                    continue
                
                self.list_of_mass_hypothesis.append(''.join(['mass_'  , l1, l2, l3]))
                self.list_of_mass_hypothesis.append(''.join(['mass12_', l1, l2]))
                self.list_of_mass_hypothesis.append(''.join(['mass13_', l1, l3]))
                self.list_of_mass_hypothesis.append(''.join(['mass23_', l2, l3]))
        ## remove duplicates arising from two-body masses 
        ## (e.g. PiPiK and PiKK would fill the  mass13_pk value twice)
        self.list_of_mass_hypothesis = list(set(self.list_of_mass_hypothesis))
        for ll in self.list_of_mass_hypothesis:
                self.var(self.tree, ll)
        
        self.hlt_triggers = set(['_'.join(tt.split('_')[:-1]) for tt in self.cfg_comp.triggers])
        for tt in self.hlt_triggers:
            self.var(self.tree, tt + '_matched', type=int, storageType='B')
            self.var(self.tree, tt + '_fired'  , type=int, storageType='B')


        # trigger information
        if hasattr(self.cfg_ana, 'fillL1') and self.cfg_ana.fillL1:
            self.bookL1object(self.tree, 'mu1_L1')
            self.bookL1object(self.tree, 'mu2_L1')
            self.bookL1object(self.tree, 'mu3_L1')
    
            self.var(self.tree, 'L1_mass12')
            self.var(self.tree, 'L1_mass13')
            self.var(self.tree, 'L1_mass23')
    
            self.var(self.tree, 'L1_dR12')
            self.var(self.tree, 'L1_dR13')
            self.var(self.tree, 'L1_dR23')
    
            self.var(self.tree, 'L1_pt12')
            self.var(self.tree, 'L1_pt13')
            self.var(self.tree, 'L1_pt23')

        # BDT output
        self.var(self.tree, 'bdt_proba')
        self.var(self.tree, 'bdt_decision')
        
        # more on weights
        self.var(self.tree, 'mu1_id_sf'   )
        self.var(self.tree, 'mu2_id_sf'   )
        self.var(self.tree, 'mu3_id_sf'   )

        self.var(self.tree, 'mu1_id_sf_e' )
        self.var(self.tree, 'mu2_id_sf_e' )
        self.var(self.tree, 'mu3_id_sf_e' )

        self.var(self.tree, 'mu1_hlt_sf'  )
        self.var(self.tree, 'mu2_hlt_sf'  )
        self.var(self.tree, 'mu3_hlt_sf'  )

        self.var(self.tree, 'mu1_hlt_sf_e')
        self.var(self.tree, 'mu2_hlt_sf_e')
        self.var(self.tree, 'mu3_hlt_sf_e')

        self.var(self.tree, 'trk_hlt_sf'  )
        self.var(self.tree, 'trk_hlt_sf_e')
        self.var(self.tree, 'dphi3d')

    def process(self, event):
        '''
        '''
        self.readCollections(event.input)
        self.tree.reset()

        if not eval(self.skimFunction):
            return False

        self.fillEvent(self.tree, event)
        self.fillTriplet(self.tree, 'cand', event.tau3mu)
        
        self.fillTriplet(self.tree, 'cand', event.tau3mu)        
        self.fillMuon(self.tree, 'mu1', event.tau3mu.mu1())
        self.fillMuon(self.tree, 'mu2', event.tau3mu.mu2())
        self.fillMuon(self.tree, 'mu3', event.tau3mu.mu3())

        self.fillTriplet(self.tree, 'cand_refit', event.tau3muRefit)
        self.fillMuon(self.tree, 'mu1_refit', event.tau3muRefit.mu1())
        self.fillMuon(self.tree, 'mu2_refit', event.tau3muRefit.mu2())
        self.fillMuon(self.tree, 'mu3_refit', event.tau3muRefit.mu3())

        if hasattr(event.tau3muRefit, 'refittedVertex') and event.tau3muRefit.refittedVertex is not None:
            self.fillVertex(self.tree, 'tau_sv', event.tau3muRefit.refittedVertex)

        # generator information
        if hasattr(event, 'genw') and event.genw is not None: 
            self.fillGenParticle(self.tree, 'gen_w', event.genw)

        if hasattr(event.tau3mu.mu1(), 'genp') and event.tau3mu.mu1().genp is not None: 
            self.fillGenParticle(self.tree, 'mu1_gen', event.tau3mu.mu1().genp)
        if hasattr(event.tau3mu.mu2(), 'genp') and event.tau3mu.mu2().genp is not None: 
            self.fillGenParticle(self.tree, 'mu2_gen', event.tau3mu.mu2().genp)
        if hasattr(event.tau3mu.mu3(), 'genp') and event.tau3mu.mu3().genp is not None: 
            self.fillGenParticle(self.tree, 'mu3_gen', event.tau3mu.mu3().genp)

        if hasattr(event, 'genmet') and event.genmet is not None: 
            self.fillParticle(self.tree, 'gen_met', event.genmet)

        if hasattr(event, 'gentau') and event.gentau is not None: 
            self.fillParticle(self.tree, 'cand_refit_gen', event.gentau)

        ## particles information
        if hasattr(event, 'HLT_tau'):
            self.fillParticle(self.tree, 'HLT_tau', event.hltmatched[0])
        
        if hasattr(event, 'ncand_hltpass'):
            self.fill(self.tree, 'ncand_hltpass', event.ncand_hltpass)

        if hasattr(event, 'dR_tau_hlt'):
            self.fill(self.tree, 'dR_tau_hlt', event.dR_tau_hlt)

        ## muon filters informations
        

        # trigger information
        if hasattr(self.cfg_ana, 'fillL1') and self.cfg_ana.fillL1:
            if hasattr(event.tau3muRefit.mu1(), 'L1'):
                self.fillL1object(self.tree, 'mu1_L1', event.tau3muRefit.mu1().L1)
            if hasattr(event.tau3muRefit.mu2(), 'L1'):
                self.fillL1object(self.tree, 'mu2_L1', event.tau3muRefit.mu2().L1)
            if hasattr(event.tau3muRefit.mu3(), 'L1'):
                self.fillL1object(self.tree, 'mu3_L1', event.tau3muRefit.mu3().L1)
    
            if hasattr(event.tau3muRefit.mu1(), 'L1') and hasattr(event.tau3muRefit.mu2(), 'L1'):

                l1mu1 = ROOT.TLorentzVector()
                l1mu1.SetPtEtaPhiM(
                    event.tau3muRefit.mu1().L1.pt(),
                    event.tau3muRefit.mu1().L1.eta(),
                    event.tau3muRefit.mu1().L1.phi(),
                    muon_mass,
                )
            
                l1mu2 = ROOT.TLorentzVector()
                l1mu2.SetPtEtaPhiM(
                    event.tau3muRefit.mu2().L1.pt(),
                    event.tau3muRefit.mu2().L1.eta(),
                    event.tau3muRefit.mu2().L1.phi(),
                    muon_mass,
                )
                        
                l1mass12 = (l1mu1 + l1mu2).M()
                l1dR12   = deltaR(l1mu1.Eta(), l1mu1.Phi(), l1mu2.Eta(), l1mu2.Phi())
                l1pt12   = (l1mu1 + l1mu2).Pt()
                
            self.fill(self.tree, 'L1_mass12', l1mass12)
            self.fill(self.tree, 'L1_dR12'  , l1dR12)
            self.fill(self.tree, 'L1_pt12'  , l1pt12)
    
            if hasattr(event.tau3muRefit.mu1(), 'L1') and hasattr(event.tau3muRefit.mu3(), 'L1'):

                l1mu1 = ROOT.TLorentzVector()
                l1mu1.SetPtEtaPhiM(
                    event.tau3muRefit.mu1().L1.pt(),
                    event.tau3muRefit.mu1().L1.eta(),
                    event.tau3muRefit.mu1().L1.phi(),
                    muon_mass,
                )
            
                l1mu3 = ROOT.TLorentzVector()
                l1mu3.SetPtEtaPhiM(
                    event.tau3muRefit.mu3().L1.pt(),
                    event.tau3muRefit.mu3().L1.eta(),
                    event.tau3muRefit.mu3().L1.phi(),
                    muon_mass,
                )
                        
                l1mass13 = (l1mu1 + l1mu3).M()
                l1dR13   = deltaR(l1mu1.Eta(), l1mu1.Phi(), l1mu3.Eta(), l1mu3.Phi())
                l1pt13   = (l1mu1 + l1mu3).Pt()
            
            self.fill(self.tree, 'L1_mass13', l1mass13)
            self.fill(self.tree, 'L1_dR13'  , l1dR13)
            self.fill(self.tree, 'L1_pt13'  , l1pt13)
    
            if hasattr(event.tau3muRefit.mu2(), 'L1') and hasattr(event.tau3muRefit.mu3(), 'L1'):

                l1mu2 = ROOT.TLorentzVector()
                l1mu2.SetPtEtaPhiM(
                    event.tau3muRefit.mu2().L1.pt(),
                    event.tau3muRefit.mu2().L1.eta(),
                    event.tau3muRefit.mu2().L1.phi(),
                    muon_mass,
                )
            
                l1mu3 = ROOT.TLorentzVector()
                l1mu3.SetPtEtaPhiM(
                    event.tau3muRefit.mu3().L1.pt(),
                    event.tau3muRefit.mu3().L1.eta(),
                    event.tau3muRefit.mu3().L1.phi(),
                    muon_mass,
                )
                        
                l1mass23 = (l1mu2 + l1mu3).M()
                l1dR23   = deltaR(l1mu2.Eta(), l1mu2.Phi(), l1mu3.Eta(), l1mu3.Phi())
                l1pt23   = (l1mu2 + l1mu3).Pt()
            
            self.fill(self.tree, 'L1_mass23', l1mass23)
            self.fill(self.tree, 'L1_dR23'  , l1dR23)
            self.fill(self.tree, 'L1_pt23'  , l1pt23)
    
        ## MET filter information
        if event.input.eventAuxiliary().isRealData():
            self.fill(self.tree, 'Flag_goodVertices'                      , event.Flag_goodVertices                      ),
            self.fill(self.tree, 'Flag_globalSuperTightHalo2016Filter'    , event.Flag_globalSuperTightHalo2016Filter    ),
            self.fill(self.tree, 'Flag_HBHENoiseFilter'                   , event.Flag_HBHENoiseFilter                   ),
            self.fill(self.tree, 'Flag_HBHENoiseIsoFilter'                , event.Flag_HBHENoiseIsoFilter                ),
            self.fill(self.tree, 'Flag_EcalDeadCellTriggerPrimitiveFilter', event.Flag_EcalDeadCellTriggerPrimitiveFilter),
            self.fill(self.tree, 'Flag_BadPFMuonFilter'                   , event.Flag_BadPFMuonFilter                   ),
            self.fill(self.tree, 'Flag_eeBadScFilter'                     , event.Flag_eeBadScFilter                     ),
            self.fill(self.tree, 'passBadMuonFilter'                      , event.passBadMuonFilter                      ),
            self.fill(self.tree, 'passBadChargedHadronFilter'             , event.passBadChargedHadronFilter             ),
            #self.fill(self.tree, 'Flag_BadChargedCandidateFilter'         , ev.Flag_BadChargedCandidateFilter        ),
            #self.fill(self.tree, 'Flag_ecalBadCalibFilter'                , ev.Flag_ecalBadCalibFilter               ),
            #self.fill(self.tree, 'ecalBadCalibReducedMINIAODFilter'       , ev.ecalBadCalibReducedMINIAODFilter      ),
    

        # BDT output
        if hasattr(event, 'bdt_proba'):
            self.fill(self.tree, 'bdt_proba', event.bdt_proba)
        if hasattr(event, 'bdt_decision'):
            self.fill(self.tree, 'bdt_decision', event.bdt_decision)
 
        # jet variables
        if len(event.cleanJets)>0:
            self.fillJet(self.tree, 'jet1', event.cleanJets[0], fill_extra=False)
        if len(event.cleanJets)>1:
            self.fillJet(self.tree, 'jet2', event.cleanJets[1], fill_extra=False)
        if len(event.cleanBJets)>0:
            self.fillJet(self.tree, 'bjet1', event.cleanBJets[0], fill_extra=False)
        if len(event.cleanBJets)>1:
            self.fillJet(self.tree, 'bjet2', event.cleanBJets[1], fill_extra=False)

        self.fill(self.tree, 'HTjets' , event.HT_cleanJets   )
        self.fill(self.tree, 'HTbjets', event.HT_bJets       )
        self.fill(self.tree, 'njets'  , len(event.cleanJets) )
        self.fill(self.tree, 'nbjets' , len(event.cleanBJets))

        ## fill resonances infos (see booking of variables)
        for ll in self.list_of_mass_hypothesis:
            self.fill(self.tree, ll, getattr(event, ll, -99))
        
        ## trigger information
        if hasattr(event.tau3mu, 'matched_triggers'):
            for tt in self.hlt_triggers:
                self.fill(self.tree, tt + '_matched', event.tau3mu.matched_triggers[tt]) if tt in event.tau3mu.matched_triggers.keys() else \
                self.fill(self.tree, tt + '_matched', False)
        if hasattr(event, 'fired_triggers'):
            fired_triggers_no_name = set(['_'.join(ft.split('_')[:-1]) for ft in event.fired_triggers])
            for tt in self.hlt_triggers:
                self.fill(self.tree, tt + '_fired', True ) if tt in fired_triggers_no_name else \
                self.fill(self.tree, tt + '_fired', False) 
        
        ## some additional BDT variables
        ##      angle between PV-SV and p(tau)
        pv = ROOT.TVector3(event.vertices[0].x(), event.vertices[0].y(), event.vertices[0].z())
        sv = ROOT.TVector3(event.tau3muRefit.refittedVertex.x(), event.tau3muRefit.refittedVertex.y(), event.tau3muRefit.refittedVertex.z())
        seg  = sv - pv
        ptau = ROOT.TVector3(event.tau3muRefit.p4().px(), event.tau3muRefit.p4().py(), event.tau3muRefit.p4().pz())
        dphi_3d = seg.Angle(ptau)
        self.fill(self.tree, 'dphi3d', dphi_3d)

        # weights
        self.fill(self.tree, 'mu1_id_sf'   , getattr(event.tau3mu.mu1(), 'idweight'      , 1.))
        self.fill(self.tree, 'mu2_id_sf'   , getattr(event.tau3mu.mu2(), 'idweight'      , 1.))
        self.fill(self.tree, 'mu3_id_sf'   , getattr(event.tau3mu.mu3(), 'idweight'      , 1.))

        self.fill(self.tree, 'mu1_id_sf_e' , getattr(event.tau3mu.mu1(), 'idweightunc'   , 0.))
        self.fill(self.tree, 'mu2_id_sf_e' , getattr(event.tau3mu.mu2(), 'idweightunc'   , 0.))
        self.fill(self.tree, 'mu3_id_sf_e' , getattr(event.tau3mu.mu3(), 'idweightunc'   , 0.))

        self.fill(self.tree, 'mu1_hlt_sf'  , getattr(event.tau3mu.mu1(), 'HLTWeightMU'   , 1.))
        self.fill(self.tree, 'mu2_hlt_sf'  , getattr(event.tau3mu.mu2(), 'HLTWeightMU'   , 1.))
        self.fill(self.tree, 'mu3_hlt_sf'  , getattr(event.tau3mu.mu3(), 'HLTWeightMU'   , 1.))

        self.fill(self.tree, 'mu1_hlt_sf_e', getattr(event.tau3mu.mu1(), 'HLTWeightUncMU', 0.))
        self.fill(self.tree, 'mu2_hlt_sf_e', getattr(event.tau3mu.mu2(), 'HLTWeightUncMU', 0.))
        self.fill(self.tree, 'mu3_hlt_sf_e', getattr(event.tau3mu.mu3(), 'HLTWeightUncMU', 0.))

        self.fill(self.tree, 'trk_hlt_sf'  , getattr(event.tau3mu      , 'HLTWeightTK'   , 1.))
        self.fill(self.tree, 'trk_hlt_sf_e', getattr(event.tau3mu      , 'HLTWeightUncTK', 0.))

        self.fillTree(event)

