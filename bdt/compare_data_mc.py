import ROOT
import math
from CMSStyle import CMS_lumi

ROOT.gStyle.SetOptStat(0)
ROOT.gROOT.SetBatch(True)

class PlotContainer(object):
    def __init__(self, var, selection, mcselection, xtitle, norm, nbins, xmin, xmax, pltopt, label=None, logx=False, logy=False, fill=False):
        self.var         = var 
        self.selection   = selection 
        self.mcselection = mcselection 
        self.xtitle      = xtitle 
        self.norm        = norm 
        self.nbins       = nbins 
        self.xmin        = xmin 
        self.xmax        = xmax
        self.pltopt      = pltopt
        self.logy        = logy
        self.logx        = logx
        self.fill        = fill
        if label:
            self.label = label
        else:
            self.label = self.var

t1 = ROOT.TChain('tree')
t1.Add('/Users/manzoni/Documents/tau3mu2018/16april/ntuples/DoubleMuonLowMass_Run2016Bv2_03Feb2017/WTau3MuTreeProducer/tree_enriched_16apr2018v16.root')
t1.Add('/Users/manzoni/Documents/tau3mu2018/16april/ntuples/DoubleMuonLowMass_Run2016C_03Feb2017/WTau3MuTreeProducer/tree_enriched_16apr2018v16.root'  )
t1.Add('/Users/manzoni/Documents/tau3mu2018/16april/ntuples/DoubleMuonLowMass_Run2016D_03Feb2017/WTau3MuTreeProducer/tree_enriched_16apr2018v16.root'  )
t1.Add('/Users/manzoni/Documents/tau3mu2018/16april/ntuples/DoubleMuonLowMass_Run2016E_03Feb2017/WTau3MuTreeProducer/tree_enriched_16apr2018v16.root'  )
t1.Add('/Users/manzoni/Documents/tau3mu2018/16april/ntuples/DoubleMuonLowMass_Run2016F_03Feb2017/WTau3MuTreeProducer/tree_enriched_16apr2018v16.root'  )
t1.Add('/Users/manzoni/Documents/tau3mu2018/16april/ntuples/DoubleMuonLowMass_Run2016G_03Feb2017/WTau3MuTreeProducer/tree_enriched_16apr2018v16.root'  )
t1.Add('/Users/manzoni/Documents/tau3mu2018/16april/ntuples/DoubleMuonLowMass_Run2016Hv2_03Feb2017/WTau3MuTreeProducer/tree_enriched_16apr2018v16.root')
t1.Add('/Users/manzoni/Documents/tau3mu2018/16april/ntuples/DoubleMuonLowMass_Run2016Hv3_03Feb2017/WTau3MuTreeProducer/tree_enriched_16apr2018v16.root')

t2 = ROOT.TChain('tree')
t2.Add('/Users/manzoni/Documents/tau3mu2018/16april/ntuples/WToTauTo3Mu/WTau3MuTreeProducer/tree_enriched_16apr2018v16.root'      )
t2.Add('/Users/manzoni/Documents/tau3mu2018/16april/ntuples/WToTauTo3Mu_M1p55/WTau3MuTreeProducer/tree_enriched_16apr2018v16.root')
t2.Add('/Users/manzoni/Documents/tau3mu2018/16april/ntuples/WToTauTo3Mu_M1p60/WTau3MuTreeProducer/tree_enriched_16apr2018v16.root')
t2.Add('/Users/manzoni/Documents/tau3mu2018/16april/ntuples/WToTauTo3Mu_M1p65/WTau3MuTreeProducer/tree_enriched_16apr2018v16.root')
t2.Add('/Users/manzoni/Documents/tau3mu2018/16april/ntuples/WToTauTo3Mu_M1p70/WTau3MuTreeProducer/tree_enriched_16apr2018v16.root')
t2.Add('/Users/manzoni/Documents/tau3mu2018/16april/ntuples/WToTauTo3Mu_M1p85/WTau3MuTreeProducer/tree_enriched_16apr2018v16.root')
t2.Add('/Users/manzoni/Documents/tau3mu2018/16april/ntuples/WToTauTo3Mu_M1p90/WTau3MuTreeProducer/tree_enriched_16apr2018v16.root')
t2.Add('/Users/manzoni/Documents/tau3mu2018/16april/ntuples/WToTauTo3Mu_M1p95/WTau3MuTreeProducer/tree_enriched_16apr2018v16.root')

sig_selection = '(  cand_refit_tau_mass > 1.6 & cand_refit_tau_mass < 2.0                                                               & abs(cand_refit_charge)==1)'
bkg_selection = '(((cand_refit_tau_mass > 1.6 & cand_refit_tau_mass < 1.72) | (cand_refit_tau_mass > 1.84 & cand_refit_tau_mass < 2.0)) & abs(cand_refit_charge)==1)'
# bkg_selection = 'abs(cand_refit_charge)!=1'

# sig_selection = '(bdt>0.8 &   cand_refit_tau_mass > 1.6 & cand_refit_tau_mass < 2.0                                                               & abs(cand_refit_charge)==1)'
# bkg_selection = '(bdt>0.8 & ((cand_refit_tau_mass > 1.6 & cand_refit_tau_mass < 1.72) | (cand_refit_tau_mass > 1.84 & cand_refit_tau_mass < 2.0)) & abs(cand_refit_charge)==1)'

toplot = [

    PlotContainer(var = 'cand_refit_tau_mass'                                                                                   , selection = bkg_selection                          , mcselection = sig_selection + '*(weight)', xtitle = '#tau mass [GeV]'                                  , norm = True, nbins = 40, xmin =  1.6, xmax =  2.0   , fill = True, pltopt = 'HIST'),
    PlotContainer(var = 'cand_refit_tau_pt'                                                                                     , selection = bkg_selection                          , mcselection = sig_selection + '*(weight)', xtitle = '#tau p_{T} [GeV]'                                 , norm = True, nbins = 20, xmin =  0  , xmax =  100   , fill = True, pltopt = 'HIST'),
    PlotContainer(var = 'cand_refit_tau_eta'                                                                                    , selection = bkg_selection                          , mcselection = sig_selection + '*(weight)', xtitle = '#tau #eta'                                        , norm = True, nbins = 10, xmin = -2.6, xmax =    2.6 , fill = True, pltopt = 'HIST'),
    PlotContainer(var = 'cand_refit_mttau'                                                                                      , selection = bkg_selection                          , mcselection = sig_selection + '*(weight)', xtitle = 'm_{T}(#tau, E_{T}^{miss}) [GeV]'                  , norm = True, nbins = 20, xmin =  0  , xmax =  150   , fill = True, pltopt = 'HIST'),
    PlotContainer(var = 'cand_refit_tau_dBetaIsoCone0p8strength0p2_rel'                                                         , selection = bkg_selection                          , mcselection = sig_selection + '*(weight)', xtitle = '#tau iso^{rel}'                                   , norm = True, nbins = 20, xmin =  0  , xmax =    1   , fill = True, pltopt = 'HIST'),
    PlotContainer(var = 'abs(cand_refit_dPhitauMET)'                                                                            , selection = bkg_selection                          , mcselection = sig_selection + '*(weight)', xtitle = '#Delta#phi(#tau, E_{T}^{miss})'                   , norm = True, nbins = 20, xmin =  0  , xmax = math.pi, fill = True, pltopt = 'HIST'),
    PlotContainer(var = 'cand_refit_met_pt'                                                                                     , selection = bkg_selection                          , mcselection = sig_selection + '*(weight)', xtitle = 'E_{T}^{miss} [GeV]'                               , norm = True, nbins = 20, xmin =  0  , xmax =  150   , fill = True, pltopt = 'HIST'),
    PlotContainer(var = 'cand_refit_w_pt'                                                                                       , selection = bkg_selection                          , mcselection = sig_selection + '*(weight)', xtitle = 'W p_{T} [GeV]'                                    , norm = True, nbins = 20, xmin =  0  , xmax =  100   , fill = True, pltopt = 'HIST'),
    PlotContainer(var = 'abs(cand_refit_mez_2-cand_refit_mez_1)'                                                                , selection = bkg_selection                          , mcselection = sig_selection + '*(weight)', xtitle = '|p_{Z,1}^{miss} - p_{Z,2}^{miss}| [GeV]'          , norm = True, nbins = 20, xmin =  0  , xmax = 2500   , fill = True, pltopt = 'HIST', label = 'pzdiff'),
    PlotContainer(var = 'cand_refit_mez_2'                                                                                      , selection = bkg_selection + ' &cand_refit_mez_2!=0', mcselection = sig_selection + '*(weight)', xtitle = 'max(p_{Z,i}) [GeV]'                               , norm = True, nbins = 20, xmin =-2500, xmax = 2500   , fill = True, pltopt = 'HIST', label = 'maxpzmiss'),
    PlotContainer(var = 'cand_refit_mez_1'                                                                                      , selection = bkg_selection + ' &cand_refit_mez_1!=0', mcselection = sig_selection + '*(weight)', xtitle = 'min(p_{Z,i}) [GeV]'                               , norm = True, nbins = 20, xmin = -400, xmax =  400   , fill = True, pltopt = 'HIST', label = 'minpzmiss'),
    PlotContainer(var = 'mu1_refit_reliso05'                                                                                    , selection = bkg_selection                          , mcselection = sig_selection + '*(weight)', xtitle = '#mu_{1} iso^{rel}'                                , norm = True, nbins = 20, xmin =  0  , xmax =    1   , fill = True, pltopt = 'HIST'),
    PlotContainer(var = 'mu2_refit_reliso05'                                                                                    , selection = bkg_selection                          , mcselection = sig_selection + '*(weight)', xtitle = '#mu_{2} iso^{rel}'                                , norm = True, nbins = 20, xmin =  0  , xmax =    1   , fill = True, pltopt = 'HIST'),
    PlotContainer(var = 'mu3_refit_reliso05'                                                                                    , selection = bkg_selection                          , mcselection = sig_selection + '*(weight)', xtitle = '#mu_{3} iso^{rel}'                                , norm = True, nbins = 20, xmin =  0  , xmax =    1   , fill = True, pltopt = 'HIST'),
    PlotContainer(var = 'abs(mu1_refit_dz)'                                                                                     , selection = bkg_selection                          , mcselection = sig_selection + '*(weight)', xtitle = '\Deltaz(#mu_{1}, PV) [cm]'                        , norm = True, nbins = 20, xmin =  0  , xmax =   24   , fill = True, pltopt = 'HIST', logy = True),
    PlotContainer(var = 'abs(mu2_refit_dz)'                                                                                     , selection = bkg_selection                          , mcselection = sig_selection + '*(weight)', xtitle = '\Deltaz(#mu_{2}, PV) [cm]'                        , norm = True, nbins = 20, xmin =  0  , xmax =   24   , fill = True, pltopt = 'HIST', logy = True),
    PlotContainer(var = 'abs(mu3_refit_dz)'                                                                                     , selection = bkg_selection                          , mcselection = sig_selection + '*(weight)', xtitle = '\Deltaz(#mu_{3}, PV) [cm]'                        , norm = True, nbins = 20, xmin =  0  , xmax =   24   , fill = True, pltopt = 'HIST', logy = True),
    PlotContainer(var = 'abs(mu1_refit_dz-mu2_refit_dz)'                                                                        , selection = bkg_selection                          , mcselection = sig_selection + '*(weight)', xtitle = '\Deltaz(#mu_{1}, #mu_{2}) [cm]'                   , norm = True, nbins = 20, xmin =  0  , xmax =    4   , fill = True, pltopt = 'HIST', logy = True),
    PlotContainer(var = 'abs(mu1_refit_dz-mu3_refit_dz)'                                                                        , selection = bkg_selection                          , mcselection = sig_selection + '*(weight)', xtitle = '\Deltaz(#mu_{1}, #mu_{3}) [cm]'                   , norm = True, nbins = 20, xmin =  0  , xmax =    4   , fill = True, pltopt = 'HIST', logy = True),
    PlotContainer(var = 'abs(mu2_refit_dz-mu3_refit_dz)'                                                                        , selection = bkg_selection                          , mcselection = sig_selection + '*(weight)', xtitle = '\Deltaz(#mu_{2}, #mu_{3}) [cm]'                   , norm = True, nbins = 20, xmin =  0  , xmax =    4   , fill = True, pltopt = 'HIST', logy = True),
    PlotContainer(var = 'tau_sv_ls'                                                                                             , selection = bkg_selection                          , mcselection = sig_selection + '*(weight)', xtitle = '3#mu SV L/#sigma'                                 , norm = True, nbins = 20, xmin =  0  , xmax =   25   , fill = True, pltopt = 'HIST'),
    PlotContainer(var = 'tau_sv_prob'                                                                                           , selection = bkg_selection                          , mcselection = sig_selection + '*(weight)', xtitle = '3#mu SV probability'                              , norm = True, nbins = 20, xmin =  0  , xmax =    1   , fill = True, pltopt = 'HIST', logy = True),
    PlotContainer(var = 'tau_sv_cos'                                                                                            , selection = bkg_selection                          , mcselection = sig_selection + '*(weight)', xtitle = '3#mu SV cos(#theta)'                              , norm = True, nbins = 20, xmin = -1  , xmax =    1   , fill = True, pltopt = 'HIST', logy = True),
    PlotContainer(var = 'HTjets'                                                                                                , selection = bkg_selection                          , mcselection = sig_selection + '*(weight)', xtitle = 'HT jets, jet p_{T} > 20 GeV [GeV]'                , norm = True, nbins = 20, xmin =  0  , xmax =  400   , fill = True, pltopt = 'HIST'),
    PlotContainer(var = 'HTbjets'                                                                                               , selection = bkg_selection                          , mcselection = sig_selection + '*(weight)', xtitle = 'HT b-jets, b-jet p_{T} > 20 GeV, medium CSV [GeV]', norm = True, nbins = 20, xmin =  0  , xmax =  200   , fill = True, pltopt = 'HIST'),
    PlotContainer(var = 'cand_refit_dRtauMuonMax'                                                                               , selection = bkg_selection                          , mcselection = sig_selection + '*(weight)', xtitle = 'max(dR(#tau, #mu_{i})'                            , norm = True, nbins = 20, xmin =  0  , xmax =    1   , fill = True, pltopt = 'HIST'),
    PlotContainer(var = 'mu1_refit_reliso05+mu2_refit_reliso05+mu3_refit_reliso05'                                              , selection = bkg_selection                          , mcselection = sig_selection + '*(weight)', xtitle = '#sumiso^{rel}_{#mu_{i}}'                          , norm = True, nbins = 20, xmin =  0  , xmax =    1   , fill = True, pltopt = 'HIST'),
    PlotContainer(var = 'mu1_refit_reliso05+mu2_refit_reliso05+mu3_refit_reliso05+cand_refit_tau_dBetaIsoCone0p8strength0p2_rel', selection = bkg_selection                          , mcselection = sig_selection + '*(weight)', xtitle = '#sumiso^{rel}_{#mu_{i}} + iso^{rel}_{#tau}'       , norm = True, nbins = 20, xmin =  0  , xmax =    1   , fill = True, pltopt = 'HIST'),
    PlotContainer(var = 'mu1_refit_muonid_soft'                                                                                 , selection = bkg_selection                          , mcselection = sig_selection + '*(weight)', xtitle = '#mu_{1} muon ID soft'                             , norm = True, nbins =  2, xmin =  0  , xmax =    2   , fill = True, pltopt = 'HIST'),
    PlotContainer(var = 'mu2_refit_muonid_soft'                                                                                 , selection = bkg_selection                          , mcselection = sig_selection + '*(weight)', xtitle = '#mu_{2} muon ID soft'                             , norm = True, nbins =  2, xmin =  0  , xmax =    2   , fill = True, pltopt = 'HIST'),
    PlotContainer(var = 'mu3_refit_muonid_soft'                                                                                 , selection = bkg_selection                          , mcselection = sig_selection + '*(weight)', xtitle = '#mu_{3} muon ID soft'                             , norm = True, nbins =  2, xmin =  0  , xmax =    2   , fill = True, pltopt = 'HIST'),
    PlotContainer(var = 'mu1_refit_muonid_loose'                                                                                , selection = bkg_selection                          , mcselection = sig_selection + '*(weight)', xtitle = '#mu_{1} muon ID loose'                            , norm = True, nbins =  2, xmin =  0  , xmax =    2   , fill = True, pltopt = 'HIST'),
    PlotContainer(var = 'mu2_refit_muonid_loose'                                                                                , selection = bkg_selection                          , mcselection = sig_selection + '*(weight)', xtitle = '#mu_{2} muon ID loose'                            , norm = True, nbins =  2, xmin =  0  , xmax =    2   , fill = True, pltopt = 'HIST'),
    PlotContainer(var = 'mu3_refit_muonid_loose'                                                                                , selection = bkg_selection                          , mcselection = sig_selection + '*(weight)', xtitle = '#mu_{3} muon ID loose'                            , norm = True, nbins =  2, xmin =  0  , xmax =    2   , fill = True, pltopt = 'HIST'),
    PlotContainer(var = 'mu1_refit_muonid_medium'                                                                               , selection = bkg_selection                          , mcselection = sig_selection + '*(weight)', xtitle = '#mu_{1} muon ID medium'                           , norm = True, nbins =  2, xmin =  0  , xmax =    2   , fill = True, pltopt = 'HIST'),
    PlotContainer(var = 'mu2_refit_muonid_medium'                                                                               , selection = bkg_selection                          , mcselection = sig_selection + '*(weight)', xtitle = '#mu_{2} muon ID medium'                           , norm = True, nbins =  2, xmin =  0  , xmax =    2   , fill = True, pltopt = 'HIST'),
    PlotContainer(var = 'mu3_refit_muonid_medium'                                                                               , selection = bkg_selection                          , mcselection = sig_selection + '*(weight)', xtitle = '#mu_{3} muon ID medium'                           , norm = True, nbins =  2, xmin =  0  , xmax =    2   , fill = True, pltopt = 'HIST'),
    PlotContainer(var = 'mu1_refit_muonid_tight'                                                                                , selection = bkg_selection                          , mcselection = sig_selection + '*(weight)', xtitle = '#mu_{1} muon ID tight'                            , norm = True, nbins =  2, xmin =  0  , xmax =    2   , fill = True, pltopt = 'HIST'),
    PlotContainer(var = 'mu2_refit_muonid_tight'                                                                                , selection = bkg_selection                          , mcselection = sig_selection + '*(weight)', xtitle = '#mu_{2} muon ID tight'                            , norm = True, nbins =  2, xmin =  0  , xmax =    2   , fill = True, pltopt = 'HIST'),
    PlotContainer(var = 'mu3_refit_muonid_tight'                                                                                , selection = bkg_selection                          , mcselection = sig_selection + '*(weight)', xtitle = '#mu_{3} muon ID tight'                            , norm = True, nbins =  2, xmin =  0  , xmax =    2   , fill = True, pltopt = 'HIST'),
    PlotContainer(var = 'mu1_refit_muonid_tightnovtx'                                                                           , selection = bkg_selection                          , mcselection = sig_selection + '*(weight)', xtitle = '#mu_{1} muon ID tightnovtx'                       , norm = True, nbins =  2, xmin =  0  , xmax =    2   , fill = True, pltopt = 'HIST'),
    PlotContainer(var = 'mu2_refit_muonid_tightnovtx'                                                                           , selection = bkg_selection                          , mcselection = sig_selection + '*(weight)', xtitle = '#mu_{2} muon ID tightnovtx'                       , norm = True, nbins =  2, xmin =  0  , xmax =    2   , fill = True, pltopt = 'HIST'),
    PlotContainer(var = 'mu3_refit_muonid_tightnovtx'                                                                           , selection = bkg_selection                          , mcselection = sig_selection + '*(weight)', xtitle = '#mu_{3} muon ID tightnovtx'                       , norm = True, nbins =  2, xmin =  0  , xmax =    2   , fill = True, pltopt = 'HIST'),
    PlotContainer(var = 'bdt'                                                                                                   , selection = bkg_selection                          , mcselection = sig_selection + '*(weight)', xtitle = 'BDT score'                                        , norm = True, nbins = 20, xmin =  0  , xmax =    1   , fill = True, pltopt = 'HIST', logy = True),
    PlotContainer(var = 'mu1ID'                                                                                                 , selection = bkg_selection                          , mcselection = sig_selection + '*(weight)', xtitle = '#mu_{1} muon ID'                                  , norm = True, nbins =  4, xmin =  0  , xmax =    4   , fill = True, pltopt = 'HIST'),
    PlotContainer(var = 'mu2ID'                                                                                                 , selection = bkg_selection                          , mcselection = sig_selection + '*(weight)', xtitle = '#mu_{2} muon ID'                                  , norm = True, nbins =  4, xmin =  0  , xmax =    4   , fill = True, pltopt = 'HIST'),
    PlotContainer(var = 'mu3ID'                                                                                                 , selection = bkg_selection                          , mcselection = sig_selection + '*(weight)', xtitle = '#mu_{3} muon ID'                                  , norm = True, nbins =  4, xmin =  0  , xmax =    4   , fill = True, pltopt = 'HIST'),
    PlotContainer(var = 'abs(mu1_z-mu2_z)'                                                                                      , selection = bkg_selection                          , mcselection = sig_selection + '*(weight)', xtitle = '#Delta z(#mu_{1}, #mu_{2}) [cm]'                  , norm = True, nbins = 20, xmin =  0  , xmax =    1   , fill = True, pltopt = 'HIST'),
    PlotContainer(var = 'abs(mu1_z-mu3_z)'                                                                                      , selection = bkg_selection                          , mcselection = sig_selection + '*(weight)', xtitle = '#Delta z(#mu_{1}, #mu_{3}) [cm]'                  , norm = True, nbins = 20, xmin =  0  , xmax =    1   , fill = True, pltopt = 'HIST'),
    PlotContainer(var = 'abs(mu2_z-mu3_z)'                                                                                      , selection = bkg_selection                          , mcselection = sig_selection + '*(weight)', xtitle = '#Delta z(#mu_{2}, #mu_{3}) [cm]'                  , norm = True, nbins = 20, xmin =  0  , xmax =    1   , fill = True, pltopt = 'HIST'),
    PlotContainer(var = 'tauEta'                                                                                                , selection = bkg_selection                          , mcselection = sig_selection + '*(weight)', xtitle = '#tau #eta category'                               , norm = True, nbins =  8, xmin =  0  , xmax =    8   , fill = True, pltopt = 'HIST'),
    PlotContainer(var = 'cand_refit_tau_pt/cand_refit_met_pt'                                                                   , selection = bkg_selection                          , mcselection = sig_selection + '*(weight)', xtitle = '#tau p_{T}/MET'                                   , norm = True, nbins = 40, xmin =  0  , xmax =  5.0   , fill = True, pltopt = 'HIST', label = 'ptbalance'),
]

c1 = ROOT.TCanvas('c1', 'c1', 700, 700)

for i, iplot in enumerate(toplot):
    
    nbins  = iplot.nbins
    xmin    = iplot.xmin  
    xmax    = iplot.xmax  
    
    sel    = iplot.selection
    mcsel  = iplot.mcselection

    var    = iplot.var
    
    h_data = ROOT.TH1F('h_data_%d'%i, '', nbins, xmin, xmax)
    h_mc   = ROOT.TH1F('h_mc_%d'  %i, '', nbins, xmin, xmax)

    h_data.SetLineColor(ROOT.kBlack)
    h_mc  .SetLineColor(ROOT.kRed  )

    xtitle = iplot.xtitle

    h_data.GetXaxis().SetTitle(xtitle)
    h_mc  .GetXaxis().SetTitle(xtitle)

    h_data.GetYaxis().SetTitle('events')
    h_mc  .GetYaxis().SetTitle('events')

    h_data.GetXaxis().SetTitleOffset(1.2)
    h_mc  .GetXaxis().SetTitleOffset(1.2)

    h_data.GetYaxis().SetTitleOffset(1.5)
    h_mc  .GetYaxis().SetTitleOffset(1.5)

    t1.Draw('%s >> %s' %(var, h_data.GetName()), '(%s)' %(sel)  , iplot.pltopt         )
    t2.Draw('%s >> %s' %(var, h_mc  .GetName()), '(%s)' %(mcsel), iplot.pltopt + 'SAME')

    if iplot.norm:
        h_data.Scale(1./h_data.Integral())
        h_mc  .Scale(1./h_mc  .Integral())

        h_data.GetYaxis().SetTitle('a.u.')
        h_mc  .GetYaxis().SetTitle('a.u.')

    ymax = max(h_data.GetMaximum(), h_mc.GetMaximum())

    h_data.SetMaximum(1.1*ymax)
    h_mc  .SetMaximum(1.1*ymax)
            
    h_data.Draw(iplot.pltopt)
    h_mc  .Draw(iplot.pltopt + 'SAME')

#     l1 = ROOT.TLegend(0.56,0.78,0.89,0.88)
    l1 = ROOT.TLegend(0.32,0.78,0.69,0.88)
#     l1.AddEntry(h_data, 'observed'  , 'l')
#     l1.AddEntry(h_mc  , 'simulation', 'l')
    l1.AddEntry(h_data, 'data sidebands'  , 'f')
    l1.AddEntry(h_mc  , 'W#rightarrow#tau#nu, #tau#rightarrow3#mu signal'      , 'f')
    l1.SetBorderSize(0)
    l1.Draw('same')

    if iplot.fill:
        h_data.SetFillStyle(3004)
        h_mc  .SetFillStyle(3005)
        h_data.SetFillColor(ROOT.kBlack)
        h_mc  .SetFillColor(ROOT.kRed  )

    if not iplot.logy:
        h_data.SetMinimum(0.)
    ROOT.gPad.SetLogx(iplot.logx)
    ROOT.gPad.SetLogy(iplot.logy)
    
    CMS_lumi(ROOT.gPad, 4, 0)
    
    ROOT.gPad.Update()
    
    c1.SaveAs('plots_data_mc/%s.pdf' %iplot.label)
#     c1.SaveAs('plots_data_mc_cut/%s.pdf' %iplot.label)


