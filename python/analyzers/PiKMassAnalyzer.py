import ROOT
from PhysicsTools.Heppy.analyzers.core.Analyzer   import Analyzer
from itertools import product

class PiKMassAnalyzer(Analyzer):
    '''
    save infos about mass(mu1, mu2, mu3) with different mass hypothesis
    KKK   , PiPiPi,
    KKPi  , KPiK  , PiKK
    PiPiK , PiKPi , KPiPi
    MuMuPi, MuPiMu, PiMuMu
    MuMuK , MuKMu , KMuMu
    '''

    def beginLoop(self, setup):
        super(PiKMassAnalyzer, self).beginLoop(setup)
        self.counters.addCounter('PiKMass')
        count = self.counters.counter('PiKMass')
        count.register('all events')

        ## PDG values for charged mesons
        self.mass_K  = 0.493677
        self.mass_Pi = 0.139570
        self.mass_Mu = 0.105658

    def process(self, event):
        self.muons = self.comp_cfg.getter(event) if hasattr(self.cfg_comp, 'getter')  else  \
                     [event.tau3muRefit.mu1(), event.tau3muRefit.mu2(), event.tau3muRefit.mu3()]
                    
        self.counters.counter('PiKMass').inc('all events')

        mk_tpl = ('k', self.mass_K )
        mp_tpl = ('p', self.mass_Pi)
        mm_tpl = ('m', self.mass_Mu)

        kp_list = [mk_tpl, mp_tpl]  ## K-Pi  list used to generate combinations
        mk_list = [mm_tpl, mk_tpl]  ## Mu-K  list used to generate combinations
        mp_list = [mm_tpl, mp_tpl]  ## Mu-Pi list used to generate combinations

        for list_of_interest in (kp_list, mp_list, mk_list):
            for (m1, m2, m3) in product(list_of_interest, repeat = 3):
                #if m1 == m2 == m3: continue
                ## only 0 or 2 muons
                if sum([obj[0] == 'm' for obj in (m1, m2, m3)]) == 1:
                    continue
                ## labels to append to event
                label   = ''.join(['mass_'  , m1[0], m2[0], m3[0]])
                label12 = ''.join(['mass12_', m1[0], m2[0]])
                label13 = ''.join(['mass13_', m1[0], m3[0]])
                label23 = ''.join(['mass23_', m2[0], m3[0]])

                par_1 = ROOT.TLorentzVector() ; par_1.SetPtEtaPhiM(self.muons[0].pt(), self.muons[0].eta(), self.muons[0].phi(), m1[1])
                par_2 = ROOT.TLorentzVector() ; par_2.SetPtEtaPhiM(self.muons[1].pt(), self.muons[1].eta(), self.muons[1].phi(), m2[1])
                par_3 = ROOT.TLorentzVector() ; par_3.SetPtEtaPhiM(self.muons[2].pt(), self.muons[2].eta(), self.muons[2].phi(), m3[1])
                
                ## three-body mass
                mass_value   = (par_1 + par_2 + par_3).M()
                ## two-body mass combinations
                mass12_value = (par_1 + par_2).M()
                mass13_value = (par_1 + par_3).M()
                mass23_value = (par_2 + par_3).M()

                ## append to the event
                if not hasattr(event, label  ): setattr(event, label  , mass_value  )
                if not hasattr(event, label12): setattr(event, label12, mass12_value)
                if not hasattr(event, label13): setattr(event, label13, mass13_value)
                if not hasattr(event, label23): setattr(event, label23, mass23_value)

        return True    
