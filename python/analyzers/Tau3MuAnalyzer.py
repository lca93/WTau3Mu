import ROOT
from itertools import product, combinations
import math
import numpy as np
from collections import OrderedDict, Counter

from PhysicsTools.Heppy.analyzers.core.Analyzer   import Analyzer
from PhysicsTools.Heppy.analyzers.core.AutoHandle import AutoHandle
from PhysicsTools.Heppy.physicsobjects.Muon       import Muon
from PhysicsTools.Heppy.physicsobjects.Electron   import Electron
from PhysicsTools.Heppy.physicsobjects.Tau        import Tau
from PhysicsTools.HeppyCore.utils.deltar          import deltaR, deltaR2

from CMGTools.WTau3Mu.physicsobjects.Tau3MuMET    import Tau3MuMET
from CMGTools.WTau3Mu.analyzers.resonances        import resonances, sigmas_to_exclude
from pdb import set_trace

class Tau3MuAnalyzer(Analyzer):
    '''
    '''

    def declareHandles(self):
        super(Tau3MuAnalyzer, self).declareHandles()

        self.handles['taus'] = AutoHandle(
            'slimmedTaus',
            'std::vector<pat::Tau>'
        )

        self.handles['electrons'] = AutoHandle(
            'slimmedElectrons',
            'std::vector<pat::Electron>'
        )

        self.handles['muons'] = AutoHandle(
            'slimmedMuons',
            'std::vector<pat::Muon>'
        )

        self.mchandles['genParticles'] = AutoHandle(
            'prunedGenParticles',
            'std::vector<reco::GenParticle>'
        )

        self.handles['puppimet'] = AutoHandle(
            'slimmedMETsPuppi',
            'std::vector<pat::MET>'
        )

        self.handles['pfmet'] = AutoHandle(
            'slimmedMETs',
            'std::vector<pat::MET>'
        )

        self.handles['mvamets'] = AutoHandle(
            ('MVAMET', 'MVAMET', 'MVAMET'),
            'std::vector<pat::MET>',
            mayFail = True # not guaranteed MVA MET is always available
        )

    def beginLoop(self, setup):
        super(Tau3MuAnalyzer, self).beginLoop(setup)
        self.counters.addCounter('Tau3Mu')
        count = self.counters.counter('Tau3Mu')
        count.register('all events')
        count.register('> 0 vertex')
        count.register('> 0 tri-muon')
        # count.register('pass resonance veto')
        count.register('m < 3 GeV')
        count.register('pass (mu, mu, mu) Z cut')
        count.register('trigger matched')

    def buildMuons(self, muons, event):
        '''
        '''
        muons = map(Muon, muons)
        for mu in muons:
            mu.associatedVertex = event.vertices[0]
        muons = [mu for mu in muons if 
                 (mu.isSoftMuon(mu.associatedVertex) or mu.isLooseMuon()) and
                 mu.pt()>1. and
                 abs(mu.eta())<=2.5]          
        return muons

    def resonanceVeto(self, muons):
        pairs = [(i,j) for i, j in combinations(muons, 2) if (i.charge()+j.charge()) == 0]
        excluded = set()
        for rmass, rwidth, _ in resonances:
            for m1, m2 in pairs:
                if m1 in excluded or m2 in excluded: continue
                delta_mass = abs( (m1.p4()+m2.p4()).M() - rmass ) / rwidth
                if delta_mass < sigmas_to_exclude:
                    excluded.add(m1)
                    excluded.add(m2)
            pairs = [(i, j) for i, j in pairs if i not in excluded and j not in excluded]
        return list(set(muons) - excluded)

    def buildElectrons(self, electrons, event):
        '''
        Used for veto
        '''
        electrons = map(Electron, electrons)
        for ele in electrons:
            ele.associatedVertex = event.vertices[0]
#         if len(electrons):
#             import pdb ; pdb.set_trace()
        electrons = [ele for ele in electrons if
                     ele.pt()>10 and
                     abs(ele.eta())<2.5 and
                     # ele.mvaIDRun2('Spring16', 'Veto') and # why?
                     #ele.mvaIDRun2('NonTrigSpring15MiniAOD', 'POG90') and
                     self.testVertex(ele) and
                     ele.passConversionVeto() and
                     ele.physObj.gsfTrack().hitPattern().numberOfAllHits(ROOT.reco.HitPattern.MISSING_INNER_HITS) <= 1 and
                     ele.relIso(iso_type='dbeta', cone_size=0.3, dbeta_factor=0.5, all_charged=0) < 0.3]
        return electrons

    def buildTaus(self, taus, event):
        '''
        '''
        taus = map(Tau, taus)
        taus = [tau for tau in taus if 
                tau.tauID('decayModeFinding') > 0.5 and
                tau.tauID('byLooseIsolationMVArun2v1DBoldDMwLT') > 0.5 and
                tau.pt()>18. and
                abs(tau.eta())<2.3 and
                self.testTauVertex(tau)]
        return map(Tau, taus)
    
    def process(self, event):
        self.readCollections(event.input)

        if not len(event.vertices):
            return False

        self.counters.counter('Tau3Mu').inc('> 0 vertex')

        event.allmuons  =                     self.handles['muons'    ].product()
        event.muons     = self.buildMuons    (self.handles['muons'    ].product(), event)
        event.electrons = self.buildElectrons(self.handles['electrons'].product(), event)
        event.taus      = self.buildTaus     (self.handles['taus'     ].product(), event)
        event.pfmet     = self.handles['pfmet'   ].product()[0]
        event.puppimet  = self.handles['puppimet'].product()[0]
        if getattr(self.cfg_ana, 'useMVAmet', False):
            event.mvamets  = self.handles['mvamets'].product()
        
        good = self.selectionSequence(event)
        
        event.selectedLeptons = [lep for lep in event.muons + event.electrons if lep.pt()>10.] #+ event.taus # useful for jet cross cleaning

        return good

    def selectionSequence(self, event):
        self.counters.counter('Tau3Mu').inc('all events')

        if len(event.muons) < 3:
            return False
        
        ## Init to True
        event.trigger_matched = True

        self.counters.counter('Tau3Mu').inc('> 0 tri-muon')

        if   getattr(self.cfg_ana, 'useMVAmet', False):
            event.tau3mus = [Tau3MuMET(triplet, event.mvamets, useMVAmet=True) for triplet in combinations(event.muons, 3)]
        elif getattr(self.cfg_ana, 'usePUPPImet', False):
            event.tau3mus = [Tau3MuMET(triplet, event.puppimet) for triplet in combinations(event.muons, 3)]
        else:
            event.tau3mus = [Tau3MuMET(triplet, event.pfmet) for triplet in combinations(event.muons, 3)]

        # testing di-lepton itself
        seltau3mu = event.tau3mus

        # mass cut
        seltau3mu = [triplet for triplet in seltau3mu if triplet.massMuons() < 3.]

        if len(seltau3mu) == 0:
            return False
        self.counters.counter('Tau3Mu').inc('m < 3 GeV')

        # max longitudinal distance among the three muons
        dzcut = getattr(self.cfg_ana, 'dz_cut', 1) # 1 cm
        
        seltau3mu_tmp = []
        
        for tt in seltau3mu:
        
            max_distance = max([ abs(tt.mu1().vz()-tt.mu2().vz()),
                                 abs(tt.mu1().vz()-tt.mu3().vz()),
                                 abs(tt.mu2().vz()-tt.mu3().vz()) ])
        
            if max_distance < dzcut:
                seltau3mu_tmp.append(tt)            

        seltau3mu = seltau3mu_tmp                       
                                            
        if len(seltau3mu) == 0:
            return False

        self.counters.counter('Tau3Mu').inc('pass (mu, mu, mu) Z cut')

        # match only if the trigger fired
        event.fired_triggers = [info.name for info in getattr(event, 'trigger_infos', []) if info.fired]

        # trigger matching
        if hasattr(self.cfg_ana, 'trigger_match') and len(self.cfg_ana.trigger_match.keys())>0:
            event.matched_triggers  = {}
            event.best_triplet      = {}
            event.best_tau          = {}
            for triplet in seltau3mu:
                muons = [triplet.mu1(), triplet.mu2(), triplet.mu3()]
                tau   = muons[0].p4() + muons[1].p4() + muons[2].p4()

                ## 2017: match only the tau
                for info in event.trigger_infos:
                    ## init the trigger matching
                    trigger_name    = '_'.join(info.name.split('_')[:-1])
                    trigger_filters = self.cfg_ana.trigger_match[trigger_name][0]

                    if not trigger_name in self.cfg_ana.trigger_match.keys(): continue

                    ## can different versions overlap?
                    event.matched_triggers[trigger_name] = False if not trigger_name in event.matched_triggers else event.matched_triggers[trigger_name]

                    ## match woth dR if the object filter is in the filters of interest
                    mu1_trigger_objs = sorted([obj for obj in info.objects if deltaR(muons[0], obj) < 0.05 and any(obj.filter(flt) for flt in trigger_filters)], key = lambda x: deltaR(x, muons[0]))
                    mu2_trigger_objs = sorted([obj for obj in info.objects if deltaR(muons[1], obj) < 0.05 and any(obj.filter(flt) for flt in trigger_filters)], key = lambda x: deltaR(x, muons[1]))
                    mu3_trigger_objs = sorted([obj for obj in info.objects if deltaR(muons[2], obj) < 0.05 and any(obj.filter(flt) for flt in trigger_filters)], key = lambda x: deltaR(x, muons[2]))
                    tau_trigger_objs = sorted([obj for obj in info.objects if deltaR(tau     , obj) < 0.05 and any(obj.filter(flt) for flt in trigger_filters)], key = lambda x: deltaR(x, tau     ))
                    
                    trigger_types_to_match = self.cfg_ana.trigger_match[trigger_name][1]
                    ## build all the possible combinations of three muons
                    hlt_matches  = [tt for tt in [mu1_trigger_objs, mu2_trigger_objs, mu3_trigger_objs] if len(tt) > 0]
                    hlt_triplets = [tt for tt in product(*hlt_matches) if len(set(tt)) >= len(self.cfg_ana.trigger_match[trigger_name][0])]
                    ## the selected triplets must match the trigger types of interest
                    hlt_triplets = [tt for tt in hlt_triplets if Counter([mu.triggerObjectTypes()[0] for mu in tt]) == trigger_types_to_match]
                    ## cut on the hlt triplet mass around the tau mass
                    hlt_triplets = [tt for tt in hlt_triplets if self.tauMass(tt) < 2.02 and self.tauMass(tt) > 1.6]
                    ## sort the hlt triplet candidates based on the distance from the offline triplet
                    hlt_triplets.sort(key = lambda x: sum([deltaR(x[jj], muons[jj]) for jj in range(3)]), reverse = False)

                    event.best_triplet[trigger_name] = hlt_triplets[0]      if len(hlt_triplets)     > 0 else None
                    event.best_tau    [trigger_name] = tau_trigger_objs[0]  if len(tau_trigger_objs) > 0 else None

                    if trigger_name == 'HLT_DoubleMu3_Trk_Tau3mu':
                        if event.best_triplet is not None:
                            event.matched_triggers[trigger_name] = True
                    else:
                        if event.best_tau is not None:
                            event.matched_triggers[trigger_name] = True

                for kk in event.matched_triggers.keys():
                    ## ignore 2016 trigger
                    if kk != 'HLT_DoubleMu3_Trk_Tau3mu':
                        continue
                    triplet.trigger_matched = event.matched_triggers[kk] or getattr(triplet, 'trigger_matched', False)

            seltau3mu = [triplet for triplet in seltau3mu if triplet.trigger_matched]
            
            if len(seltau3mu) == 0:
                return False
                
        self.counters.counter('Tau3Mu').inc('trigger matched')
        event.seltau3mu = seltau3mu
        event.tau3mu = self.bestTriplet(event.seltau3mu)

        return True

    def bestTriplet(self, triplets):
        '''
        The best triplet is the one with the correct charge and highest mT(3mu, MET). 
        If there are more than one triplets with the wrong charge, take the one with the highest  mT(3mu, MET).
        '''
        triplets.sort(key=lambda tt : (abs(tt.charge())==1, tt.mttau()), reverse=True)    
        return triplets[0]
    
    def testVertex(self, lepton):
        '''Tests vertex constraints, for mu'''
        return abs(lepton.dxy()) < 0.045 and abs(lepton.dz()) < 0.2
        
    def testTauVertex(self, tau):
        '''Tests vertex constraints, for tau'''
        # Just checks if the primary vertex the tau was reconstructed with
        # corresponds to the one used in the analysis
        # isPV = abs(tau.vertex().z() - tau.associatedVertex.z()) < 0.2
        isPV = abs(tau.leadChargedHadrCand().dz()) < 0.2
        return isPV

    
