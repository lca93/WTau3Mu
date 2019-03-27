#! /bin/env python

import ROOT
import os
from math import pi, sqrt
from glob import glob
from pdb import set_trace
from array import array 
import math
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--basedir'   , dest='basedir'   , default='../cfgPython')
parser.add_argument('--jobid'     , dest='jobid'     , default='')
parser.add_argument('--selection' , dest='selection' , default='bdt>0.89 & abs(cand_charge)==1')
# parser.add_argument('--signalnorm', dest='signalnorm', default=33183./20000.*21490.9*1E-7) # normalize to BR = 1E-7. In this formula: lumi / ngen events * pp->W, BR W->taunu * BR tau->3mu

# http://inspirehep.net/record/1604393/files/SMP-15-004-pas.pdf
# measured cross section multiplied by BR(W->taunu) / BR(W->munu)
parser.add_argument('--signalnorm'    , dest='signalnorm'    , default=33183./20000.*(8580+11370)*0.1138/0.1063*1E-7)
parser.add_argument('--category'      , dest='category'      , default='')
parser.add_argument('--datafile'      , dest='datafile'      , default='data_skimmed.root')
parser.add_argument('--sigfile'       , dest='sigfile'       , default='signal.root')
parser.add_argument('--blinded'       , dest='blinded'       , action='store_true' )
parser.add_argument('--unblinded'     , dest='blinded'       , action='store_false')
parser.add_argument('--nbins'         , dest='nbins'         , default=40)
parser.add_argument('--mass_window_lo', dest='mass_window_lo', default=1.72)
parser.add_argument('--mass_window_hi', dest='mass_window_hi', default=1.84)
parser.add_argument('--fit_range_lo'  , dest='fit_range_lo'  , default=1.62)
parser.add_argument('--fit_range_hi'  , dest='fit_range_hi'  , default=1.98)
parser.set_defaults(blinded=True)

args = parser.parse_args() 

blinded        = args.blinded
selection      = args.selection
nbins          = args.nbins
mass_window_lo = args.mass_window_lo
mass_window_hi = args.mass_window_hi
fit_range_lo   = args.fit_range_lo
fit_range_hi   = args.fit_range_hi

# ROOT.gROOT.SetBatch()
ROOT.gStyle.SetOptStat(True)
ROOT.TH1.SetDefaultSumw2()

##########################################################################################
##      Pick up the MC tree
##########################################################################################

# Load MC file
if not args.sigfile:
    mc_file = '%s/%s/WToTauTo3Mu/WTau3MuTreeProducer/tree.root' % (args.basedir, args.jobid)
    if not os.path.isfile(mc_file):
       raise IOError('I could not find the input MC file: %s' % mc_file)
else:
    mc_file = args.sigfile

if len(args.category)>0:
    args.category = '_'+args.category

gaus = ROOT.TF1('signalgaus', 'gaus', 1.7, 1.86)
   
mc_file = ROOT.TFile.Open(mc_file)
mc_file.cd()
mc_tree = mc_file.Get('tree')

# get the integral
mass_histo_mc = ROOT.TH1F('mass_histo_mc', 'mass_histo_mc', nbins, 1.6, 2.)
mc_tree.Draw('cand_refit_tau_mass>>mass_histo_mc', '(' + selection + ') * weight * %f' %args.signalnorm)

##########################################################################################
##      Pick up the observed tree
##########################################################################################

# Load data files
if not args.datafile:
    data_files = glob('%s/%s/DoubleMuonLowMass_*/WTau3MuTreeProducer/tree.root'% (args.basedir, args.jobid))
    if not data_files:
       raise IOError('I could not find any data file in the %s/%s directory' % (args.basedir, args.jobid))
else:
    data_files = [args.datafile]
print 'found %d input files' % len(data_files)

data_tree = ROOT.TChain('tree')
for fname in data_files:
   data_tree.AddFile(fname)

##########################################################################################
#      Variables and PDFs
##########################################################################################
# mass_  = ROOT.RooRealVar('cand_refit_tau_mass', '3-#mu mass'          , 1.6, 2, 'GeV')
# mass   = ROOT.RooRealVar(mass_, 'mass')
# mass   = ROOT.RooRealVar('cand_refit_tau_mass', '3-#mu mass'          , 1.6, 2, 'GeV')
mass      = ROOT.RooRealVar('cand_refit_tau_mass', '3-#mu mass'          , 1.6, 2, 'GeV')
bdt       = ROOT.RooRealVar('bdt'                , 'bdt'                 , -1 , 1)
charge    = ROOT.RooRealVar('cand_charge'        , 'charge'              , -4 , 4)
weight    = ROOT.RooRealVar('mcweight'           , 'mcweight'            ,  0., 5)
eta       = ROOT.RooRealVar('cand_refit_tau_eta' , 'cand_refit_tau_eta'  , -5., 5)
mass12ref = ROOT.RooRealVar('cand_refit_mass12'  , 'cand_refit_mass12'   ,  0., 2)
mass13ref = ROOT.RooRealVar('cand_refit_mass13'  , 'cand_refit_mass13'   ,  0., 2)
mass23ref = ROOT.RooRealVar('cand_refit_mass23'  , 'cand_refit_mass23'   ,  0., 2)
mass12    = ROOT.RooRealVar('cand_mass12'        , 'cand_mass12'         ,  0., 2)
mass13    = ROOT.RooRealVar('cand_mass13'        , 'cand_mass13'         ,  0., 2)
mass23    = ROOT.RooRealVar('cand_mass23'        , 'cand_mass23'         ,  0., 2)
charge12  = ROOT.RooRealVar('cand_charge12'      , 'cand_charge12'       , -3 , 3)
charge13  = ROOT.RooRealVar('cand_charge13'      , 'cand_charge13'       , -3 , 3)
charge23  = ROOT.RooRealVar('cand_charge23'      , 'cand_charge23'       , -3 , 3)
mu1_trig_type = ROOT.RooRealVar('mu1_hlt_doublemu3_trk_tau3mu_type'      , 'mu1_hlt_doublemu3_trk_tau3mu_type'       , 0 , 100)
mu2_trig_type = ROOT.RooRealVar('mu2_hlt_doublemu3_trk_tau3mu_type'      , 'mu2_hlt_doublemu3_trk_tau3mu_type'       , 0 , 100)
mu3_trig_type = ROOT.RooRealVar('mu3_hlt_doublemu3_trk_tau3mu_type'      , 'mu3_hlt_doublemu3_trk_tau3mu_type'       , 0 , 100)
# scale  = ROOT.RooRealVar('mcscale'            , 'mcscale'   , signal_norm)

mass.setRange('left' , fit_range_lo  , mass_window_lo)
mass.setRange('right', mass_window_hi, fit_range_hi  )

# PDF
slope = ROOT.RooRealVar('slope', 'slope', -0.001, -1e6, 1e6)
expo  = ROOT.RooExponential('bkg_expo', 'bkg_expo', mass, slope)

slope2 = ROOT.RooRealVar('slope2', 'slope2', -0.001, -1e6, 1e6)
# expo2  = ROOT.RooExponential('bkg_expo2', 'bkg_expo2', mass, slope2)
expo2  = ROOT.RooExponential('bkg_expo2', 'bkg_expo2', mass, slope)

# number of background events
nbkg = ROOT.RooRealVar('nbkg', 'nbkg', 1000, 0, 550000)
# see this https://root-forum.cern.ch/t/fit-only-the-sidebands-yield-on-full-range-using-rooextendpdf/31868
expomodel = ROOT.RooAddPdf('bkg_extended_expo', 'bkg_extended_expo', ROOT.RooArgList(expo), ROOT.RooArgList(nbkg))

##
mean  = ROOT.RooRealVar('mean' , 'mean' ,   1.78, -1.7, 1.9)
width = ROOT.RooRealVar('width', 'width',   0.02,    0, 0.1)
gaus  = ROOT.RooGaussian('sig_gaus', 'sig_gaus', mass, mean, width)

thevars = ROOT.RooArgSet()
thevars.add(mass)
thevars.add(bdt )
thevars.add(charge)
thevars.add(weight)
thevars.add(eta)
thevars.add(mass12ref)
thevars.add(mass13ref)
thevars.add(mass23ref)
thevars.add(mass12)
thevars.add(mass13)
thevars.add(mass23)
thevars.add(charge12)
thevars.add(charge13)
thevars.add(charge23)
thevars.add(mu1_trig_type)
thevars.add(mu2_trig_type)
thevars.add(mu3_trig_type)

##########################################################################################
# selection on MC, weight application, plotting, fitting
##########################################################################################

fullmc = ROOT.RooDataSet('mc', 'mc', mc_tree, thevars, selection, 'mcweight')

frame = mass.frame()
frame.SetTitle('')

fullmc  .plotOn(frame, 
                ROOT.RooFit.Binning(nbins), 
                ROOT.RooFit.DrawOption('B'), 
                ROOT.RooFit.DataError(ROOT.RooAbsData.None), 
                ROOT.RooFit.XErrorSize(0), 
                ROOT.RooFit.LineWidth(2),
                ROOT.RooFit.FillColor(ROOT.kRed),
                ROOT.RooFit.FillStyle(3003),                
                )
results_gaus = gaus.fitTo(fullmc, ROOT.RooFit.Range(mass_window_lo,mass_window_hi), ROOT.RooFit.Save())
# results_gaus = gaus.fitTo(fullmc, ROOT.RooFit.Save(), ROOT.RooFit.SumW2Error(True))
# results_gaus = gaus.chi2FitTo(fullmc, ROOT.RooFit.Save())
gaus.plotOn(frame, ROOT.RooFit.LineColor(ROOT.kRed))

##########################################################################################
# selection on data, plotting, fitting
##########################################################################################

if blinded:
    print 'BLIND'
    # cut for blinding
    blinder = ROOT.RooFormulaVar('blinder', 'blinder', selection + ' & abs(cand_refit_tau_mass-1.78)>0.06', ROOT.RooArgList(thevars))
    fulldata = ROOT.RooDataSet('data', 'data', data_tree,  thevars, blinder)
else:
    print 'NOW I SEE'
    fulldata = ROOT.RooDataSet('data', 'data', data_tree,  thevars, selection)

fulldata.plotOn(frame, ROOT.RooFit.Binning(nbins), ROOT.RooFit.MarkerSize(1.))
results_expo = expomodel.fitTo(fulldata, ROOT.RooFit.Range('left,right'), ROOT.RooFit.Save())
# expo.plotOn(frame, ROOT.RooFit.LineColor(ROOT.kBlack))
expomodel.plotOn(frame, ROOT.RooFit.LineColor(ROOT.kBlue))

##
# results_expo2 = expo2.fitTo(fulldata, ROOT.RooFit.Range('left,right'), ROOT.RooFit.Save())
# expo2.plotOn(frame, ROOT.RooFit.LineColor(ROOT.kOrange))



# number of background events
# nbkg1 = ROOT.RooRealVar  ('nbkg1', 'nbkg1', 1000, 0, 550000)
# extend the expo to the full range
# mass.setRange('full', 1.61, 1.99)
# ebkg = ROOT.RooExtendPdf('ebkg','ebkg', expo, nbkg1, 'full') 
# ebkg.fitTo(fulldata, ROOT.RooFit.Range('left,right'))
# ebkg.plotOn(frame, ROOT.RooFit.LineColor(ROOT.kBlue))

frame.Draw()
ROOT.gPad.SaveAs('mass%s_%dbins.pdf'%(args.category, nbins))

##########################################################################################
#  Dump the RooFit Workspace
##########################################################################################
# create output file
output = ROOT.TFile.Open('datacard%s.root' %args.category, 'recreate')
seldata = ROOT.RooDataSet('data', 'data', data_tree, thevars, selection)

# use more convenient names NOT WORKING !!
# mass.SetNameTitle('mass', 'mass')

print 'dumping data'
data =  ROOT.RooDataSet(
    'data_obs', 
    'data_obs',
    seldata, 
    ROOT.RooArgSet(mass)
)

# create workspace
print 'creating workspace'
w = ROOT.RooWorkspace('t3m_shapes')

# dump linear parametrization of bkg
# peek at the factory syntax
# https://agenda.infn.it/getFile.py/access?contribId=15&resId=0&materialId=slides&confId=5719

# exponential
# w.factory('mass[%f, %f]' % (1.61, 1.99))
# w.factory("Exponential::bkg(mass, a0%s[%f,%f,%f])" %(args.category, slope.getVal(), slope.getError(), slope.getError()) )  
w.factory('cand_refit_tau_mass[%f, %f]' % (fit_range_lo, fit_range_hi))
w.factory("Exponential::bkg(cand_refit_tau_mass, a0%s[%f,%f,%f])" %(args.category, slope.getVal(), slope.getError(), slope.getError()) )  

# dump signal with fixed shape (the final fit will only vary the normalisation
w.factory('mean[%f]'  % mean .getVal())
w.factory('sigma[%f]' % width.getVal())
# w.factory('RooGaussian::sig(mass, mean, sigma)')
w.factory('RooGaussian::sig(cand_refit_tau_mass, mean, sigma)')

# in order to fix the shape, loop over the variables and fix mean and sigma 
it = w.allVars().createIterator()
all_vars = [it.Next() for _ in range( w.allVars().getSize())]
for var in all_vars:
    if var.GetName() in ['mean', 'sigma']:
        var.setConstant()

getattr(w,'import')(data)
w.Write()
output.Close()

# import pdb ; pdb.set_trace()

# dump the datacard
with open('datacard%s.txt' %args.category, 'w') as card:
   card.write(
'''
imax 1 number of bins
jmax * number of processes minus 1
kmax * number of nuisance parameters
--------------------------------------------------------------------------------
shapes background    Wtau3mu{cat}       datacard{cat}.root t3m_shapes:bkg
shapes signal        Wtau3mu{cat}       datacard{cat}.root t3m_shapes:sig
shapes data_obs      Wtau3mu{cat}       datacard{cat}.root t3m_shapes:data_obs
--------------------------------------------------------------------------------
bin               Wtau3mu{cat}
observation       {obs:d}
--------------------------------------------------------------------------------
bin                                     Wtau3mu{cat}        Wtau3mu{cat}
process                                 signal              background
process                                 0                   1
rate                                    {signal:.4f}        {bkg:.4f}
--------------------------------------------------------------------------------
lumi          lnN                       1.025               -   
xs_W          lnN                       1.037               -   
br_Wtaunu     lnN                       1.0021              -   
br_Wmunu      lnN                       1.0015              -   
mc_stat{cat}  lnN                       {mcstat:.4f}        -   
mu_id{cat}    lnN                       {mu_id:.4f}         -   
mu_hlt{cat}   lnN                       {mu_hlt:.4f}        -   
trk_hlt{cat}  lnN                       {trk_hlt:.4f}       -   
hlt_extrap    lnN                       1.05                -   
--------------------------------------------------------------------------------
bkgNorm{cat}  rateParam                 Wtau3mu{cat}        background      1.
a0{cat}       param   {slopeval:.4f} {slopeerr:.4f}
'''.format(
         cat      = args.category,
         obs      = fulldata.numEntries() if blinded==False else -1,
         signal   = mass_histo_mc.Integral(),
         bkg      = nbkg.getVal(),
         mcstat   = 1. + sqrt(mass_histo_mc.Integral()/args.signalnorm)/mass_histo_mc.Integral()*args.signalnorm,
         mu_id    = 1.044  if 'barrel' in args.category else 1.078,
         mu_hlt   = 1.012  if 'barrel' in args.category else 1.040,
         trk_hlt  = 1.0086 if 'barrel' in args.category else 1.0086,
         slopeval = slope.getVal(), 
         slopeerr = slope.getError(),
         )
)
