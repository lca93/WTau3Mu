from copy import deepcopy as dc
import ROOT

from PhysicsTools.Heppy.analyzers.core.Analyzer   import Analyzer
from PhysicsTools.Heppy.analyzers.core.AutoHandle import AutoHandle
from PhysicsTools.HeppyCore.utils.deltar          import deltaR, bestMatch

from CMGTools.WTau3Mu.physicsobjects.DsPhiMuMuPi  import DsPhiMuMuPi

class DsPhiMuMuPiGenMatcherAnalyzer(Analyzer):
    '''
    '''


    def declareHandles(self):
        super(DsPhiMuMuPiGenMatcherAnalyzer, self).declareHandles()
        
        self.mchandles['packedGenParticles'] = AutoHandle(
            'packedGenParticles',
            'std::vector<pat::PackedGenParticle>'
        )

    def process(self, event):
        if event.input.eventAuxiliary().isRealData():
            return True

        self.readCollections(event.input)
   
        # packed gen particles
        packed_gen_particles = self.mchandles['packedGenParticles'].product()
    
        # match the ds to gen ds
        muons = self.cfg_ana.getter(event)
        tau_p4 = muons[0].p4() + muons[1].p4() + muons[2].p4()

        # get all Ds in the event
        gends = [pp for pp in event.genParticles if abs(pp.pdgId())==431]
        gends = [pp for pp in gends if [13, 13, 211] == sorted([abs(dd.pdgId()) for dd in self.finalDaughters(pp)])]

        ## match the Ds
        the_ds, dRmin_ds = bestMatch(tau_p4, gends)

        event.matched_ds = (dRmin_ds < 0.1)
        event.gentau = the_ds

        if event.gentau is not None:
            event.gentau.deltaPt = the_ds.pt() - tau_p4.pt()
            
            ## match the daughters
            gen_muons = [pp for pp in self.finalDaughters(event.gentau) if abs(pp.pdgId()) == 13 ]
            gen_pion  = [pp for pp in self.finalDaughters(event.gentau) if abs(pp.pdgId()) == 211]
            gen_phi   = [pp for pp in [the_ds.daughter(ii) for ii in range(the_ds.numberOfDaughters())] if abs(pp.pdgId()) == 333]

            genp_mu1, dRmin_mu1 = bestMatch(muons[0], gen_muons + gen_pion)
            genp_mu2, dRmin_mu2 = bestMatch(muons[1], [pp for pp in (gen_muons + gen_pion) if pp is not genp_mu1])
            genp_mu3, dRmin_mu3 = bestMatch(muons[2], [pp for pp in (gen_muons + gen_pion) if pp is not genp_mu1 and pp is not genp_mu2])

            event.matched_mu1 = (dRmin_mu1 < 0.1)
            event.matched_mu2 = (dRmin_mu2 < 0.1)
            event.matched_mu3 = (dRmin_mu3 < 0.1)

            muons[0].genp = genp_mu1
            muons[1].genp = genp_mu2
            muons[2].genp = genp_mu3

            if muons[0].genp is not None:
                muons[0].genp.dRmin = dRmin_mu1
                muons[0].genp.deltaPt = muons[0].genp.pt() - muons[0].pt()
            
            if muons[1].genp is not None:
                muons[1].genp.dRmin = dRmin_mu2
                muons[1].genp.deltaPt = muons[1].genp.pt() - muons[1].pt()
            
            if muons[2].genp is not None:
                muons[2].genp.dRmin = dRmin_mu3
                muons[2].genp.deltaPt = muons[2].genp.pt() - muons[2].pt()


            reco_muons = [mu for mu in muons if abs(mu.genp.pdgId()) == 13]
            if len(reco_muons) == 2:
                reco_phi = reco_muons[0].p4() + reco_muons[1].p4()
                genp_phi, dRmin_phi = bestMatch(reco_phi, gen_phi)
            else:
                genp_phi = None
                dRmin_phi = 99
            
            event.matched_phi = dRmin_phi < 0.1
            
            event.genphi = genp_phi

            if event.genphi is not None:
                event.genphi.dRmin = dRmin_phi
                event.genphi.deltaPt = event.genphi.pt() - reco_phi.pt()

        '''
        # restrict to only those that decay into phi pi
        gends = [pp for pp in gends if pp.numberOfDaughters()==2 and (len(set([333, 211]) & set([abs(pp.daughter(0).pdgId()), abs(pp.daughter(1).pdgId())]))==2)]
        
        # append to the event the gen level Ds Phi Mu Mu Phi with the highest momentum
        gends.sort(key = lambda x : x.pt(), reverse=True)
        try:
            mygends = gends[0]  
        except:
            import pdb ; pdb.set_trace()
        mygends.phip = [dau for dau in [mygends.daughter(ii)      for ii in range(mygends.numberOfDaughters())     ] if abs(dau.pdgId())==333][0]  
        mygends.pi   = [dau for dau in [mygends.daughter(ii)      for ii in range(mygends.numberOfDaughters())     ] if abs(dau.pdgId())==211][0]  
        mygends.mum  = [mu  for mu  in [mygends.phip.daughter(ii) for ii in range(mygends.phip.numberOfDaughters())] if     mu .pdgId() == 13][0]  
        mygends.mup  = [mu  for mu  in [mygends.phip.daughter(ii) for ii in range(mygends.phip.numberOfDaughters())] if     mu .pdgId() ==-13][0]  
        event.gends  = DsPhiMuMuPi([mygends.mum, mygends.mup], mygends.pi)
        event.ngends = len(gends)
                
        # match the reco candidate to the gen Ds
        best_match, dRmin = bestMatch(dsphimumupi, gends)
        ds_match = best_match if dRmin < 0.3 else None
        if ds_match:
            ds_match.phip = [pp for pp in [ds_match.daughter(0), ds_match.daughter(1)] if pp.pdgId()==333][0]
                    
        muons = [dsphimumupi.mu1(), dsphimumupi.mu2()]          
        
        # now match the two muons and the pion: 
        #    first try to match to any stable gen particle
        stableGenParticles = [pp for pp in event.genParticles if pp.status()==1]
        for mu in muons + [dsphimumupi.pi()]:
            best_match, dRmin = bestMatch(mu, stableGenParticles)
            if dRmin < 0.1:
                mu.genp = best_match
            
        #     then match to phi daughters
        #     but only if the reco ds is matched to a gen ds itself
        if ds_match:
            # append the gen ds to the event
            event.ds.genp = ds_match
            muons_from_phi = [mu for mu in [ds_match.phip.daughter(ii) for ii in range(ds_match.phip.numberOfDaughters())] if abs(mu.pdgId())==13]
            for mu in muons_from_phi:
                best_match, dRmin = bestMatch(mu, muons)
                if dRmin < 0.1:
                    best_match.genp = mu
        
        neutrinos = [pp for pp in event.genParticles if abs(pp.pdgId()) in [12, 14, 16] and pp.status()==1]
        
        for i, nn in enumerate(neutrinos):
            if i==0:
                event.genmet = nn.p4()
            else:
                event.genmet += nn.p4()
        '''
        return True
    
    @staticmethod
    def finalDaughters(gen, daughters=None):
        if daughters is None:
            daughters = []
        for i in range(gen.numberOfDaughters()):
            daughter = gen.daughter(i)
            if daughter.numberOfDaughters() == 0:
                daughters.append(daughter)
            else:
                DsPhiMuMuPiGenMatcherAnalyzer.finalDaughters(daughter, daughters)
        return daughters


    @staticmethod
    def isAncestor(a, p):
        if a == p :
            return True
        for i in xrange(0,p.numberOfMothers()):
            if DsPhiMuMuPiGenMatcherAnalyzer.isAncestor(a,p.mother(i)):
                return True
        return False

