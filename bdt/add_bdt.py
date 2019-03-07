import ROOT
import root_pandas
import numpy as np
import pandas as pd
import xgboost as xgb
import pandas, root_numpy
from sklearn.externals import joblib
from sklearn import preprocessing
import matplotlib.pyplot as plt 

@np.vectorize
def muID(loose, medium, tight):
    if   tight  > 0.5: return 3
    elif medium > 0.5: return 2
    elif loose  > 0.5: return 1
    else             : return 0

@np.vectorize
def tauEta(eta):
    if   abs(eta) > 2.1 : return 7
    elif abs(eta) > 1.8 : return 6
    elif abs(eta) > 1.5 : return 5
    elif abs(eta) > 1.1 : return 4
    elif abs(eta) > 0.8 : return 3
    elif abs(eta) > 0.5 : return 2
    elif abs(eta) > 0.2 : return 1
    else                : return 0

# tag = '5mar2019_v4' # legacy BDT
tag = '16apr2018_v16' # new BDTs

# classifiers = joblib.load('bdt/classifiers_%s.pck' %tag)
classifiers = joblib.load('../classifiers/classifiers_%s.pck' %tag)

# 16apr2018v16
features = [
    'cand_refit_tau_pt',
    'cand_refit_mttau',
    'cand_refit_tau_dBetaIsoCone0p8strength0p2_rel',
    'abs(cand_refit_dPhitauMET)',
    'cand_refit_met_pt',
#     'cand_refit_tau_pt*(cand_refit_met_pt**-1)', # only for >= v4
#     'cand_refit_tau_pt/cand_refit_met_pt', # only for >= v2
#     'cand_refit_dRtauMuonMax',
    'cand_refit_w_pt',
    'cand_refit_mez_1',
    'cand_refit_mez_2',
    'abs(mu1_z-mu2_z)', 
    'abs(mu1_z-mu3_z)', 
    'abs(mu2_z-mu3_z)',
    'tau_sv_ls',
    'tau_sv_prob',
    'tau_sv_cos',
    'mu1ID',
    'mu2ID',
    'mu3ID',
    'tauEta',
]

ifiles = [
    '/Users/manzoni/Documents/tau3mu2018/5mar2019/ntuples/WToTauTo3Mu/WTau3MuTreeProducer/tree.root',
    '/Users/manzoni/Documents/tau3mu2018/5mar2019/ntuples/WToTauTo3Mu_M1p55/WTau3MuTreeProducer/tree.root',
    '/Users/manzoni/Documents/tau3mu2018/5mar2019/ntuples/WToTauTo3Mu_M1p60/WTau3MuTreeProducer/tree.root',
    '/Users/manzoni/Documents/tau3mu2018/5mar2019/ntuples/WToTauTo3Mu_M1p65/WTau3MuTreeProducer/tree.root',
    '/Users/manzoni/Documents/tau3mu2018/5mar2019/ntuples/WToTauTo3Mu_M1p70/WTau3MuTreeProducer/tree.root',
    '/Users/manzoni/Documents/tau3mu2018/5mar2019/ntuples/WToTauTo3Mu_M1p85/WTau3MuTreeProducer/tree.root',
    '/Users/manzoni/Documents/tau3mu2018/5mar2019/ntuples/WToTauTo3Mu_M1p90/WTau3MuTreeProducer/tree.root',
    '/Users/manzoni/Documents/tau3mu2018/5mar2019/ntuples/WToTauTo3Mu_M1p95/WTau3MuTreeProducer/tree.root',
    '/Users/manzoni/Documents/tau3mu2018/5mar2019/ntuples/DoubleMuonLowMass_Run2016Bv2_03Feb2017/WTau3MuTreeProducer/tree.root',
    '/Users/manzoni/Documents/tau3mu2018/5mar2019/ntuples/DoubleMuonLowMass_Run2016C_03Feb2017/WTau3MuTreeProducer/tree.root',
    '/Users/manzoni/Documents/tau3mu2018/5mar2019/ntuples/DoubleMuonLowMass_Run2016D_03Feb2017/WTau3MuTreeProducer/tree.root',
    '/Users/manzoni/Documents/tau3mu2018/5mar2019/ntuples/DoubleMuonLowMass_Run2016E_03Feb2017/WTau3MuTreeProducer/tree.root',
    '/Users/manzoni/Documents/tau3mu2018/5mar2019/ntuples/DoubleMuonLowMass_Run2016F_03Feb2017/WTau3MuTreeProducer/tree.root',
    '/Users/manzoni/Documents/tau3mu2018/5mar2019/ntuples/DoubleMuonLowMass_Run2016G_03Feb2017/WTau3MuTreeProducer/tree.root',
    '/Users/manzoni/Documents/tau3mu2018/5mar2019/ntuples/DoubleMuonLowMass_Run2016Hv2_03Feb2017/WTau3MuTreeProducer/tree.root',
    '/Users/manzoni/Documents/tau3mu2018/5mar2019/ntuples/DoubleMuonLowMass_Run2016Hv3_03Feb2017/WTau3MuTreeProducer/tree.root',
]


for ifile in ifiles:

    print 'loading dataset...'
    dataset = pandas.DataFrame(root_numpy.root2array(ifile, 'tree'))
    print '\t...done'

    dataset['bdt'] = np.zeros_like(dataset.event)

    for mu in [1,2,3]:
        name = 'mu%iID' % mu
        dataset[name] = muID(
            dataset['mu%d_refit_muonid_loose'  % mu], 
            dataset['mu%d_refit_muonid_medium' % mu], 
            dataset['mu%d_refit_muonid_tight'  % mu],
        )
        
    dataset['tauEta'                                   ] = tauEta(dataset['cand_refit_tau_eta'])
    dataset['abs(cand_refit_dPhitauMET)'               ] = abs(dataset['cand_refit_dPhitauMET'])
    dataset['abs(mu1_z-mu2_z)'                         ] = abs(dataset['mu1_z']-dataset['mu2_z'])
    dataset['abs(mu1_z-mu3_z)'                         ] = abs(dataset['mu1_z']-dataset['mu3_z'])
    dataset['abs(mu2_z-mu3_z)'                         ] = abs(dataset['mu2_z']-dataset['mu3_z'])
    dataset['cand_refit_tau_pt*(cand_refit_met_pt**-1)'] = dataset['cand_refit_tau_pt']/dataset['cand_refit_met_pt']
#     dataset['cand_refit_tau_pt/cand_refit_met_pt'] = dataset['cand_refit_tau_pt']/dataset['cand_refit_met_pt']
    dataset['mcweight'                           ] = dataset['weight']*35900./20000.*(8580+11370)*0.1138/0.1063*1E-7

    n_class = len(classifiers)

    for i, iclas in classifiers.iteritems():
        print 'computing probabilities for %d-th classifier' %i
        bdt_proba = iclas.predict_proba(dataset[features])[:,1]
        dataset['bdt'     ] += bdt_proba/n_class
        dataset['bdt_%d'%i]  = bdt_proba
        print '\t...done'


    newfile = '/'.join(ifile.split('/')[:-1] + ['tree_enriched_%s.root' %tag])
#     newfile = '/'.join(ifile.split('/')[:-1] + ['wjets_enriched_%s.root' %tag])
#     newfile = '/'.join(ifile.split('/')[:-1] + ['dyjets_enriched_%s.root' %tag])
#     newfile = '/'.join(ifile.split('/')[:-1] + ['ewk_enriched_%s.root' %tag])
#     newfile = '/'.join(ifile.split('/')[:-1] + ['ds_enriched_%s.root' %tag])
#     newfile = '/'.join(ifile.split('/')[:-1] + ['single_mu_enriched_%s.root' %tag])
#     newfile = '/'.join(ifile.split('/')[:-1] + ['signal_single_mu_enriched_%s.root' %tag])
#     newfile = '/'.join(ifile.split('/')[:-1] + ['data_test_enriched_%s.root' %tag])
#     newfile = '/'.join(ifile.split('/')[:-1] + ['data_train_enriched_%s.root' %tag])
#     newfile = '/'.join(ifile.split('/')[:-1] + ['data_21jan19_enriched_%s.root' %tag])
#     newfile = '/'.join(ifile.split('/')[:-1] + ['signal_21jan19_enriched_%s.root' %tag])

    dataset.to_root(newfile, key='tree', store_index=False)
