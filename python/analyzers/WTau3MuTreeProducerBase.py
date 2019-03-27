from PhysicsTools.Heppy.analyzers.core.TreeAnalyzerNumpy import TreeAnalyzerNumpy
from CMGTools.WTau3Mu.analyzers.TreeVariables import event_vars, triplet_vars, vertex_vars, particle_vars, lepton_vars, electron_vars, muon_vars, tau_vars, tau_vars_extra, jet_vars, jet_vars_extra, geninfo_vars, l1obj_vars
from CMGTools.H2TauTau.proto.physicsobjects.DiObject import DiTau

class WTau3MuTreeProducerBase(TreeAnalyzerNumpy):

    '''
    '''

    def __init__(self, *args):
        super(WTau3MuTreeProducerBase, self).__init__(*args)
        self.skimFunction = 'True'
        if hasattr(self.cfg_ana, 'skimFunction'):
            self.skimFunction = self.cfg_ana.skimFunction

    def var(self, tree, varName, type=float, storageType='default'):
        tree.var(varName, type = type, storageType = storageType)

    def vars(self, tree, varNames, type=float):
        for varName in varNames:
            self.var(tree, varName, type)

    def fill(self, tree, varName, value):
        tree.fill(varName, value)

    def fillVars(self, tree, varNames, obj):
        '''Fills vars that are attributes of the passed object.
        Fills -999. if object doesn't have attribute'''
        for varName in varNames:
            tree.fill(varName, getattr(obj, varName, -999.))

    def fillTree(self, event):
        if eval(self.skimFunction):
            self.tree.tree.Fill()

    def bookGeneric(self, tree, var_list, obj_name=None):
        for var in var_list:
            names = [obj_name, var.name] if obj_name else [var.name]
            self.var(tree, '_'.join(names), type = var.type, storageType = var.storageType)

    def fillGeneric(self, tree, var_list, obj, obj_name=None):
        for var in var_list:
            names = [obj_name, var.name] if obj_name else [var.name]
            try:
                self.fill(tree, '_'.join(names), var.function(obj))
            except TypeError:
                print 'Problem in filling value into tree'
                print var.name, var.function(obj), obj
                raise

    def declareVariables(self, setup):
        ''' Declare all variables here in derived calss
        '''
        pass

    def process(self, event):
        ''' Fill variables here in derived class

        End implementation with self.fillTree(event)
        '''
        # needed when doing handle.product(), goes back to
        # PhysicsTools.Heppy.analyzers.core.Analyzer
        self.tree.reset()

        if not eval(self.skimFunction):
            return False

        # self.fillTree(event)

    # event
    def bookEvent(self, tree):
        self.bookGeneric(tree, event_vars)

    def fillEvent(self, tree, event):
        self.fillGeneric(tree, event_vars, event)

    # triplet
    def bookTriplet(self, tree, p_name):
        self.bookGeneric(tree, triplet_vars, p_name)

    def fillTriplet(self, tree, p_name, particle):
        self.fillGeneric(tree, triplet_vars, particle, p_name)

    # vertex
    def bookVertex(self, tree, p_name):
        self.bookGeneric(tree, vertex_vars, p_name)

    def fillVertex(self, tree, p_name, particle):
        self.fillGeneric(tree, vertex_vars, particle, p_name)

    # simple particle
    def bookParticle(self, tree, p_name):
        self.bookGeneric(tree, particle_vars, p_name)

    def fillParticle(self, tree, p_name, particle):
        self.fillGeneric(tree, particle_vars, particle, p_name)

    # simple gen particle
    def bookGenParticle(self, tree, p_name):
        self.bookParticle(tree, p_name)
        self.var(tree, '{p_name}_pdgId'.format(p_name=p_name))

    def fillGenParticle(self, tree, p_name, particle):
        self.fillParticle(tree, p_name, particle)
        self.fill(tree, '{p_name}_pdgId'.format(p_name=p_name), particle.pdgId() if not hasattr(particle, 'detFlavour') else particle.detFlavour)

    # stage-2 L1 object
    def bookL1object(self, tree, p_name):
        self.bookParticle(tree, p_name)
        self.bookGeneric(tree, l1obj_vars, p_name)

    # stage-2 L1 object
    def fillL1object(self, tree, p_name, l1obj):
        self.fillParticle(tree, p_name, l1obj)
        self.fillGeneric(tree, l1obj_vars, l1obj, p_name)

    # lepton
    def bookLepton(self, tree, p_name):
        self.bookParticle(tree, p_name)
        self.bookParticle(tree, p_name + '_jet')
        self.bookGeneric(tree, lepton_vars, p_name)

    def fillLepton(self, tree, p_name, lepton):
        self.fillParticle(tree, p_name, lepton)
        if hasattr(lepton, 'jet'):
            self.fillParticle(tree, p_name + '_jet', lepton.jet)
        self.fillGeneric(tree, lepton_vars, lepton, p_name)

    # muon
    def bookMuon(self, tree, p_name):
        self.bookLepton(tree, p_name)
        self.bookGeneric(tree, muon_vars, p_name)

    def fillMuon(self, tree, p_name, muon):
        self.fillLepton(tree, p_name, muon)
        self.fillGeneric(tree, muon_vars, muon, p_name)

    # ele
    def bookEle(self, tree, p_name):
        self.bookLepton(tree, p_name)
        self.bookGeneric(tree, electron_vars, p_name)

    def fillEle(self, tree, p_name, ele):
        self.fillLepton(tree, p_name, ele)
        self.fillGeneric(tree, electron_vars, ele, p_name)

    # tau
    def bookTau(self, tree, p_name, fill_extra=False):
        self.bookLepton(tree, p_name)
        self.bookGeneric(tree, tau_vars, p_name)
        if fill_extra:
            self.bookGeneric(tree, tau_vars_extra, p_name)

    def fillTau(self, tree, p_name, tau, fill_extra=False):
        self.fillLepton(tree, p_name, tau)
        self.fillGeneric(tree, tau_vars, tau, p_name)
        if fill_extra:
            self.fillGeneric(tree, tau_vars_extra, tau, p_name)

    # jet
    def bookJet(self, tree, p_name, fill_extra=False):
        self.bookParticle(tree, p_name)
        self.bookGeneric(tree, jet_vars, p_name)
        if fill_extra:
            self.bookGeneric(tree, jet_vars_extra, p_name)

    def fillJet(self, tree, p_name, jet, fill_extra=False):
        self.fillParticle(tree, p_name, jet)
        self.fillGeneric(tree, jet_vars, jet, p_name)
        if fill_extra:
            self.fillGeneric(tree, jet_vars_extra, jet, p_name)

    # generator information
    def bookGenInfo(self, tree):
        self.bookGeneric(tree, geninfo_vars)

    def fillGenInfo(self, tree, event):
        self.fillGeneric(tree, geninfo_vars, event)

    # additional METs
    def bookExtraMetInfo(self, tree):
        self.var(tree, 'puppimet_pt')
        self.var(tree, 'puppimet_phi')
        self.var(tree, 'puppimet_mt1')
        self.var(tree, 'puppimet_mt2')
        self.var(tree, 'puppimet_mttotal')

        self.var(tree, 'pfmet_pt')
        self.var(tree, 'pfmet_phi')
        self.var(tree, 'pfmet_mt1')
        self.var(tree, 'pfmet_mt2')
        self.var(tree, 'pfmet_mttotal')

    def fillExtraMetInfo(self, tree, event):
        self.fill(tree, 'puppimet_pt', event.puppimet.pt())
        self.fill(tree, 'puppimet_phi', event.puppimet.phi())
        self.fill(tree, 'puppimet_mt1', DiTau.calcMT(event.puppimet, event.leg1))
        self.fill(tree, 'puppimet_mt2', DiTau.calcMT(event.puppimet, event.leg2))

        self.fill(tree, 'pfmet_pt', event.pfmet.pt())
        self.fill(tree, 'pfmet_phi', event.pfmet.phi())
        self.fill(tree, 'pfmet_mt1', DiTau.calcMT(event.pfmet, event.leg1))
        self.fill(tree, 'pfmet_mt2', DiTau.calcMT(event.pfmet, event.leg2))
