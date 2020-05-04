import ROOT

from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer
from PhysicsTools.HeppyCore.utils.deltar        import bestMatch

class qcdGenMatcherAnalyzer(Analyzer):
    '''
    gen-match muons and try to gen match the tau
    '''
    def process(self, event):
        if event.input.eventAuxiliary().isRealData():
            return True
        
        tau3mu = self.cfg_ana.getter(event)
        tau = tau3mu.p4Muons()
        
        stableGenParticles = [pp for pp in event.genParticles if pp.status()==1]
        
        muons = sorted([tau3mu.mu1(), tau3mu.mu2(), tau3mu.mu3()], key = lambda mu: mu.pt(), reverse = True)
        
        for mu in muons:
            best_match, dRmin = bestMatch(mu, stableGenParticles)
            
            if dRmin < 0.1:
                mu.genp = best_match
                stableGenParticles = [gp for gp in stableGenParticles if not gp is mu.genp]
        
        event.gentau, _ = bestMatch(tau, stableGenParticles)

        return True
