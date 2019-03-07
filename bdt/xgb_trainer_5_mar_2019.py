# import pandas
import root_numpy
import argparse
import pickle
import numpy  as np
import pandas as pd
import seaborn as sns
from sklearn.metrics import accuracy_score
# import matplotlib as mpl ; mpl.use('Agg')
import matplotlib.pyplot as plt
# sns.set(style="whitegrid", font_scale=2)
sns.set(style="white")

import xgboost
from xgboost import XGBClassifier, plot_importance

from sklearn.metrics         import roc_curve, roc_auc_score
from sklearn.model_selection import train_test_split, StratifiedKFold
from sklearn.externals       import joblib

from scipy.stats import ks_2samp

from collections import OrderedDict
from itertools import product

from pdb import set_trace

##########################################################################################
# https://www.dataiku.com/learn/guide/code/python/advanced-xgboost-tuning.html

# give labels human readable names
labels = OrderedDict()

labels['cand_refit_tau_pt'                            ] = '$\\tau$ $p_{T}$'
labels['cand_refit_mttau'                             ] = '$m_{T}(\\tau, MET)$'
labels['cand_refit_tau_dBetaIsoCone0p8strength0p2_rel'] = '$\\tau$ iso'
labels['abs(cand_refit_dPhitauMET)'                   ] = '$\Delta\phi(\\tau MET)$'
labels['cand_refit_met_pt'                            ] = 'MET $p_{T}$'
# labels['cand_refit_tau_pt/cand_refit_met_pt'          ] = '$\\tau$ $p_{T}$/MET $p_{T}$' # only for >= v2
labels['cand_refit_tau_pt*(cand_refit_met_pt**-1)'    ] = '$\\tau$ $p_{T}$/MET $p_{T}$' # only for >= v2
# labels['cand_refit_dRtauMuonMax'                      ] = 'max($\Delta R(\\tau \mu_{i})$)'
labels['cand_refit_w_pt'                              ] = 'W $p_{T}$'
labels['cand_refit_mez_1'                             ] = '$max(ME_z^i)$'
labels['cand_refit_mez_2'                             ] = '$min(ME_z^i)$'
labels['abs(mu1_z-mu2_z)'                             ] = '$\Delta z (\mu_1, \mu_2)$'
labels['abs(mu1_z-mu3_z)'                             ] = '$\Delta z (\mu_1, \mu_3)$'
labels['abs(mu2_z-mu3_z)'                             ] = '$\Delta z (\mu_2, \mu_3)$'
labels['tau_sv_ls'                                    ] = 'SV L/$\sigma$'
labels['tau_sv_prob'                                  ] = 'SV prob'
labels['tau_sv_cos'                                   ] = 'SV cos($\\theta_{IP}$)'
labels['mu1ID'                                        ] = '$\mu_1$ ID'
labels['mu2ID'                                        ] = '$\mu_2$ ID'
labels['mu3ID'                                        ] = '$\mu_3$ ID'
labels['tauEta'                                       ] = '$|\eta_{\\tau}|$'
labels['bdt'                                          ] = 'BDT'
labels['cand_refit_tau_mass'                          ] = '$\\tau$ mass'

##########################################################################################
# Define the gini metric - from https://www.kaggle.com/c/ClaimPredictionChallenge/discussion/703#5897
def gini(actual, pred, cmpcol = 0, sortcol = 1):
    assert( len(actual) == len(pred) )
    all = np.asarray(np.c_[ actual, pred, np.arange(len(actual)) ], dtype=np.float)
    all = all[ np.lexsort((all[:,2], -1*all[:,1])) ]
    totalLosses = all[:,0].sum()
    giniSum = all[:,0].cumsum().sum() / totalLosses
    
    giniSum -= (len(actual) + 1) / 2.
    return giniSum / len(actual)
 
def gini_normalized(a, p):
    return gini(a, p) / gini(a, a)

def gini_xgb(preds, dtrain):
    labels = dtrain.get_label()
    gini_score = gini_normalized(labels, preds)
    return 'gini', gini_score

##########################################################################################
tag = '5mar2019_v4'
##########################################################################################

parser = argparse.ArgumentParser()
parser.add_argument('--load', help='load pkl instead of training')

args = parser.parse_args()

##########################################################################################
features = [
    'cand_refit_tau_pt',
    'cand_refit_mttau',
    'cand_refit_tau_dBetaIsoCone0p8strength0p2_rel',
    'abs(cand_refit_dPhitauMET)',
    'cand_refit_met_pt',
    'cand_refit_tau_pt*(cand_refit_met_pt**-1)', # only for >= v4
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
]

branches = features + [
    'cand_refit_charge',
    'cand_refit_tau_eta',
    'cand_refit_tau_mass',
    'mu1_refit_muonid_soft', 'mu1_refit_muonid_loose', 'mu1_refit_muonid_medium', 'mu1_refit_muonid_tight',
    'mu2_refit_muonid_soft', 'mu2_refit_muonid_loose', 'mu2_refit_muonid_medium', 'mu2_refit_muonid_tight',
    'mu3_refit_muonid_soft', 'mu3_refit_muonid_loose', 'mu3_refit_muonid_medium', 'mu3_refit_muonid_tight',
]

##########################################################################################

sig_selection = '(  cand_refit_tau_mass > 1.6 & cand_refit_tau_mass < 2.0                                                               & abs(cand_refit_charge)==1)'
bkg_selection = '(((cand_refit_tau_mass > 1.6 & cand_refit_tau_mass < 1.72) | (cand_refit_tau_mass > 1.84 & cand_refit_tau_mass < 2.0)) & abs(cand_refit_charge)==1)'

##########################################################################################

signals     = [
    '/Users/manzoni/Documents/tau3mu2018/5mar2019/ntuples/WToTauTo3Mu/WTau3MuTreeProducer/tree.root',
    '/Users/manzoni/Documents/tau3mu2018/5mar2019/ntuples/WToTauTo3Mu_M1p55/WTau3MuTreeProducer/tree.root',
    '/Users/manzoni/Documents/tau3mu2018/5mar2019/ntuples/WToTauTo3Mu_M1p60/WTau3MuTreeProducer/tree.root',
    '/Users/manzoni/Documents/tau3mu2018/5mar2019/ntuples/WToTauTo3Mu_M1p65/WTau3MuTreeProducer/tree.root',
    '/Users/manzoni/Documents/tau3mu2018/5mar2019/ntuples/WToTauTo3Mu_M1p70/WTau3MuTreeProducer/tree.root',
    '/Users/manzoni/Documents/tau3mu2018/5mar2019/ntuples/WToTauTo3Mu_M1p85/WTau3MuTreeProducer/tree.root',
    '/Users/manzoni/Documents/tau3mu2018/5mar2019/ntuples/WToTauTo3Mu_M1p90/WTau3MuTreeProducer/tree.root',
    '/Users/manzoni/Documents/tau3mu2018/5mar2019/ntuples/WToTauTo3Mu_M1p95/WTau3MuTreeProducer/tree.root',
]

backgrounds = [
    '/Users/manzoni/Documents/tau3mu2018/5mar2019/ntuples/DoubleMuonLowMass_Run2016Bv2_03Feb2017/WTau3MuTreeProducer/tree.root',
    '/Users/manzoni/Documents/tau3mu2018/5mar2019/ntuples/DoubleMuonLowMass_Run2016C_03Feb2017/WTau3MuTreeProducer/tree.root',
    '/Users/manzoni/Documents/tau3mu2018/5mar2019/ntuples/DoubleMuonLowMass_Run2016D_03Feb2017/WTau3MuTreeProducer/tree.root',
    '/Users/manzoni/Documents/tau3mu2018/5mar2019/ntuples/DoubleMuonLowMass_Run2016E_03Feb2017/WTau3MuTreeProducer/tree.root',
    '/Users/manzoni/Documents/tau3mu2018/5mar2019/ntuples/DoubleMuonLowMass_Run2016F_03Feb2017/WTau3MuTreeProducer/tree.root',
    '/Users/manzoni/Documents/tau3mu2018/5mar2019/ntuples/DoubleMuonLowMass_Run2016G_03Feb2017/WTau3MuTreeProducer/tree.root',
    '/Users/manzoni/Documents/tau3mu2018/5mar2019/ntuples/DoubleMuonLowMass_Run2016Hv2_03Feb2017/WTau3MuTreeProducer/tree.root',
    '/Users/manzoni/Documents/tau3mu2018/5mar2019/ntuples/DoubleMuonLowMass_Run2016Hv3_03Feb2017/WTau3MuTreeProducer/tree.root',
]

sig = pd.DataFrame( root_numpy.root2array(signals    , 'tree', branches  = branches + ['weight'], selection = sig_selection) )
bkg = pd.DataFrame( root_numpy.root2array(backgrounds, 'tree', branches  = branches + ['weight'], selection = bkg_selection) )

##########################################################################################
## DEFINE TARGETS
##########################################################################################

sig['target'] = np.ones (sig.shape[0]).astype(np.int)
bkg['target'] = np.zeros(bkg.shape[0]).astype(np.int)

##########################################################################################
## WEIGHT A BIT MORE EVENTS AT LOWER MASSES, AS THERE'S LESS
########################################################################################## 
# @np.vectorize
# def massWeighter(mass):
#     # slope
#     m = (1.15 - 0.85) / (1.6-2)    
#     # intercept
#     q = 2.35
#     return m * mass + q
# 
# sig['weight'] *= massWeighter(sig['cand_refit_tau_mass'])
# bkg['weight'] *= massWeighter(bkg['cand_refit_tau_mass'])

##########################################################################################
## REWEIGHT AND MAKE TAU MASS FLAT
########################################################################################## 
sig_integral = np.sum(sig['weight'])
bkg_integral = np.sum(bkg['weight'])

bins = np.linspace(1.6, 2, 40)

sig_mass_sum_weight = []
bkg_mass_sum_weight = []

for ibin in range(len(bins)-1):
    m_min = bins[ibin]
    m_max = bins[ibin+1]
    
    sig_mass_sum_weight.append( np.sum(sig[sig.cand_refit_tau_mass>=m_min][sig.cand_refit_tau_mass<m_max]['weight']) )
    bkg_mass_sum_weight.append( np.sum(bkg[bkg.cand_refit_tau_mass>=m_min][bkg.cand_refit_tau_mass<m_max]['weight']) )

sig_mass_weights = np.array(sig_mass_sum_weight) / sig_integral
bkg_mass_weights = np.array(bkg_mass_sum_weight) / bkg_integral

@np.vectorize
def massWeighterSig(mass):
    bin_low = np.max(np.where(mass>=bins))
    return sig_mass_weights[bin_low]

@np.vectorize
def massWeighterBkg(mass):
    bin_low = np.max(np.where(mass>=bins))
    return bkg_mass_weights[bin_low]
    
sig['weight'] /= massWeighterSig(sig['cand_refit_tau_mass'])
bkg['weight'] /= massWeighterBkg(bkg['cand_refit_tau_mass'])

# further weight adjustment
sig['weight'] *= 1.
bkg['weight'] *= 0.01

##########################################################################################
#####   COMPACTIFY AND ADD THE (POG) MUON ID TO THE SAMPLES
##########################################################################################
@np.vectorize
def muID(loose, medium, tight):
	if   tight  > 0.5: return 3
	elif medium > 0.5: return 2
	elif loose  > 0.5: return 1
	else             : return 0

for mu in [1,2,3]:
	name = 'mu%iID' % mu
	features.append(name)
	sig[name] = muID(
		sig['mu%d_refit_muonid_loose'  % mu], 
		sig['mu%d_refit_muonid_medium' % mu], 
		sig['mu%d_refit_muonid_tight'  % mu],
	)
	bkg[name] = muID(
		bkg['mu%d_refit_muonid_loose'  % mu], 
		bkg['mu%d_refit_muonid_medium' % mu], 
		bkg['mu%d_refit_muonid_tight'  % mu],
	)
	
##########################################################################################
#####   ETA BINS
##########################################################################################
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
    
features.append('tauEta')
sig['tauEta'] = tauEta(sig['cand_refit_tau_eta'])
bkg['tauEta'] = tauEta(bkg['cand_refit_tau_eta'])

##########################################################################################
data = pd.concat([sig, bkg])
data['id'] = np.arange(len(data))

train, test = train_test_split(data, test_size=0.4, random_state=1986)

##########################################################################################
kfold = 6
skf = StratifiedKFold(n_splits=kfold, random_state=1986, shuffle=True)

##########################################################################################
sub = pd.DataFrame()
sub['id']     = test.id
sub['target'] = test.target
sub['score']  = np.zeros_like(test.id)

classifier_file = open('classifiers_%s.pck' % tag, 'w+')
classifiers = OrderedDict()

# https://www.kaggle.com/sudosudoohio/stratified-kfold-xgboost-eda-tutorial-0-281
for i, (train_index, test_index) in enumerate(skf.split(train[features].values, train['target'].values)):
#     if i>2: break
    print('[Fold %d/%d]' % (i + 1, kfold))    
    X_train, X_valid = train[train.id.isin(train_index)][features], train[train.id.isin(test_index)][features]
    y_train, y_valid = train[train.id.isin(train_index)]['target'], train[train.id.isin(test_index)]['target']
    
    # Train the model! We pass in a max of 1,600 rounds (with early stopping after 70)
    # and the custom metric (maximize=True tells xgb that higher metric is better)
    clf = XGBClassifier(#silent = False)
        max_depth        = 8,
        learning_rate    = 0.005, # 0.01
        n_estimators     = 1000, # 400
        silent           = False,
        subsample        = 0.6,
        colsample_bytree = 0.7,
        min_child_weight = 1E-6 * np.sum(train[train.id.isin(train_index)].weight),
        gamma            = 10, # 20
        seed             = 1986,
        # scale_pos_weight = 0.5,
        reg_alpha        = 0.6,
        reg_lambda       = 1.2,
    )

    clf.fit(
        X_train, 
        y_train,
        eval_set              = [(X_train, y_train), (X_valid, y_valid)],
        early_stopping_rounds = 100,
        eval_metric           = 'auc',
        verbose               = True,
        sample_weight         = train['weight'],
    )
    
    classifiers[i] = clf
    
    print('[Fold %d/%d Prediciton:]' % (i + 1, kfold))
    # Predict on our test data
    p_test = clf.predict_proba(test[features])[:, 1]
    sub['score'] += p_test/kfold

    # adjust the score to match 0,1
    smin = min(p_test)
    smax = max(p_test)

    sub['score_norm'] = (p_test - smin) / (smax - smin)

    print 'round %d' %(i+1)
    print '\tcross validation error      %.5f' %(np.sum(np.abs(sub['score_norm'] - sub['target']))/len(sub))
    print '\tcross validation signal     %.5f' %(np.sum(np.abs(sub[sub.target>0.5]['score_norm'] - sub[sub.target>0.5]['target']))/len(sub))
    print '\tcross validation background %.5f' %(np.sum(np.abs(sub[sub.target<0.5]['score_norm'] - sub[sub.target<0.5]['target']))/len(sub))

    smin = min(sub['score'])
    smax = max(sub['score'])
    
    sub['score_i'] = (sub['score'] - smin) / (smax - smin)

    print 'global score as of round %d' %(i+1)
    print '\tcross validation error      %.5f' %(np.sum(np.abs(sub['score_i'] - sub['target']))/len(sub))
    print '\tcross validation signal     %.5f' %(np.sum(np.abs(sub[sub.target>0.5]['score_i'] - sub[sub.target>0.5]['target']))/len(sub))
    print '\tcross validation background %.5f' %(np.sum(np.abs(sub[sub.target<0.5]['score_i'] - sub[sub.target<0.5]['target']))/len(sub))

pickle.dump(classifiers, classifier_file)
classifier_file.close()

##########################################################################################
n_class = len(classifiers)

train['bdt'] = np.zeros_like(train.cand_refit_tau_mass)
test ['bdt'] = np.zeros_like(test .cand_refit_tau_mass)
sig  ['bdt'] = np.zeros_like(sig.cand_refit_tau_mass)
bkg  ['bdt'] = np.zeros_like(bkg.cand_refit_tau_mass)

for i, iclas in classifiers.iteritems():
    print 'evaluating the %d-th classifier' %i
    train['bdt_fold%d' %i] = iclas.predict_proba(train[features])[:, 1]
    test ['bdt_fold%d' %i] = iclas.predict_proba(test [features])[:, 1]
    sig  ['bdt_fold%d' %i] = iclas.predict_proba(sig[features])[:, 1]
    bkg  ['bdt_fold%d' %i] = iclas.predict_proba(bkg[features])[:, 1]

    train['bdt'] += iclas.predict_proba(train[features])[:, 1] / n_class
    test ['bdt'] += iclas.predict_proba(test [features])[:, 1] / n_class
    sig  ['bdt'] += iclas.predict_proba(sig[features])[:, 1] / n_class
    bkg  ['bdt'] += iclas.predict_proba(bkg[features])[:, 1] / n_class

# print '=================================>'
# print  

# plt.clf()
# aa = sns.distplot(bkg.bdt_fold0)
# bb = sns.distplot(bkg.bdt_fold1)
# cc = sns.distplot(bkg.bdt_fold2)
# aa.set_yscale('log')
# bb.set_yscale('log')
# cc.set_yscale('log')
# plt.savefig('histo.pdf')
# exit()

##########################################################################################
#####   ROC CURVE
##########################################################################################
plt.clf()

cuts_to_display = [0.80, 0.82, 0.84, 0.86, 0.89]

xy = [i*j for i,j in product([10.**i for i in range(-8, 0)], [1,2,4,8])]+[1]
plt.plot(xy, xy, color='grey', linestyle='--')
plt.xlim([10**-5, 1.0])
plt.ylim([0.0, 1.0])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')

plt.xscale('log')

fpr, tpr, wps = roc_curve(test.target, test.bdt, sample_weight=test.weight)
plt.plot(fpr, tpr, label='test sample', color='b')

wp_x = []
wp_y = []

for icut in cuts_to_display:
    idx = (wps>icut).sum()
    wp_x.append(fpr[idx])
    wp_y.append(tpr[idx])
    
plt.scatter(wp_x, wp_y)
for i, note in enumerate(cuts_to_display):
    plt.annotate(note, (wp_x[i], wp_y[i]))

fpr, tpr, wps = roc_curve(train.target, train.bdt, sample_weight=train.weight)
plt.plot(fpr, tpr, label='train sample', color='r')

wp_x = []
wp_y = []

for icut in cuts_to_display:
    idx = (wps>icut).sum()
    wp_x.append(fpr[idx])
    wp_y.append(tpr[idx])
    
plt.scatter(wp_x, wp_y)
for i, note in enumerate(cuts_to_display):
    plt.annotate(note, (wp_x[i], wp_y[i]))

print 'ROC AUC train ', roc_auc_score(train.target, train.bdt, sample_weight=train.weight)
print 'ROC AUC test  ', roc_auc_score(test.target , test.bdt , sample_weight=test.weight)

plt.legend(loc='best')
plt.grid()
plt.title('ROC')
plt.tight_layout()
plt.savefig('roc_%s.pdf' %tag)
plt.clf()

roc_file = open('roc_%s.pck' % tag, 'w+')
pickle.dump((tpr, fpr), roc_file)
roc_file.close()

##########################################################################################
#####   OVERTRAINING TEST
##########################################################################################
train_sig = train[train.target>0.5].bdt
train_bkg = train[train.target<0.5].bdt

test_sig = test[test.target>0.5].bdt
test_bkg = test[test.target<0.5].bdt

low  = 0
high = 1
low_high = (low,high)
bins = 50


#################################################
hist, bins = np.histogram(
    test_sig,
    bins=bins, 
#     range=low_high, 
    normed=True
)

width  = (bins[1] - bins[0])
center = (bins[:-1] + bins[1:]) / 2
scale  = len(test_sig) / sum(hist)
err    = np.sqrt(hist * scale) / scale

plt.errorbar(
    center, 
    hist, 
    yerr=err, 
    fmt='o', 
    c='r', 
    label='S (test)'
)

#################################################
sns.distplot(train_sig, bins=bins, kde=False, rug=False, norm_hist=True, hist_kws={"alpha": 0.5, "color": "r"}, label='S (train)')

#################################################
hist, bins = np.histogram(
    test_bkg,
    bins=bins, 
#     range=low_high, 
    normed=True
)

width  = (bins[1] - bins[0])
center = (bins[:-1] + bins[1:]) / 2
scale  = len(test_bkg) / sum(hist)
err    = np.sqrt(hist * scale) / scale

plt.errorbar(
    center, 
    hist, 
    yerr=err, 
    fmt='o', 
    c='b', 
    label='B (test)'
)

#################################################
sns.distplot(train_bkg, bins=bins, kde=False, rug=False, norm_hist=True, hist_kws={"alpha": 0.5, "color": "b"}, label='B (train)')

#################################################
plt.xlabel('BDT output')
plt.ylabel('Arbitrary units')
plt.legend(loc='best')
ks_sig = ks_2samp(train_sig, test_sig)
ks_bkg = ks_2samp(train_bkg, test_bkg)
plt.suptitle('KS p-value: sig = %.3f%s - bkg = %.2f%s' %(ks_sig.pvalue * 100., '%', ks_bkg.pvalue * 100., '%'))

# train_sig_w = np.ones_like(train_sig) * 1./len(train_sig)
# train_bkg_w = np.ones_like(train_bkg) * 1./len(train_bkg)
# test_sig_w  = np.ones_like(test_sig)  * 1./len(test_sig )
# test_bkg_w  = np.ones_like(test_bkg)  * 1./len(test_bkg )
# 
# ks_sig = ks_w2(train_sig, test_sig, train_sig_w, test_sig_w)
# ks_bkg = ks_w2(train_bkg, test_bkg, train_bkg_w, test_bkg_w)
# plt.suptitle('KS p-value: sig = %.3f%s - bkg = %.2f%s' %(ks_sig * 100., '%', ks_bkg * 100., '%'))

plt.savefig('overtrain_%s.pdf' %tag)

plt.yscale('log')

plt.savefig('overtrain_log_%s.pdf' %tag)

plt.clf()
##########################################################################################
#####   FEATURE IMPORTANCE
##########################################################################################
fscores = OrderedDict(zip(features, np.zeros(len(features))))

for i, iclas in classifiers.iteritems():
    myscores = iclas.booster().get_fscore()
    for jj in myscores.keys():
        fscores[jj] += myscores[jj]

totalsplits = np.sum(fscores.values())

for k, v in fscores.iteritems():
    fscores[k] = v/totalsplits 

plt.xlabel('relative F-score')
plt.ylabel('feature')

orderedfscores = OrderedDict(sorted(fscores.iteritems(), key=lambda x : x[1], reverse=False ))

bars = [labels[k] for k in orderedfscores.keys()]
y_pos = np.arange(len(bars))
 
# Create horizontal bars
plt.barh(y_pos, orderedfscores.values())
 
# Create names on the y-axis
plt.yticks(y_pos, bars)

# plot_importance(clf)
plt.tight_layout()
plt.savefig('feat_importance_%s.pdf' %tag)
plt.clf()

# 
# ##########################################################################################
# #####   OVERTRAINING SCORE
# ##########################################################################################
# plt.clf()
# 
# auc_train = clf.evals_result()['validation_0']['auc']
# auc_test  = clf.evals_result()['validation_1']['auc']
# 
# n_estimators = np.arange(len(auc_train))
# 
# plt.plot(n_estimators, auc_train, color='r', label='AUC train')
# plt.plot(n_estimators, auc_test , color='b', label='AUC test' )
# 
# plt.xlabel('# tree')
# plt.ylabel('Area Under ROC')
# 
# plt.xscale('log')
# # plt.yscale('log')
# plt.tight_layout()
# plt.grid()
# 
# # plt.xlim([1, 1000])
# # plt.ylim([0.985, 1.0])
# plt.ylim([0.95, 1.0])
# 
# plt.legend(loc='best')
# 
# plt.savefig('auc_score_%s.pdf' %tag)
# plt.clf()

##########################################################################################
#####   CORRELATION MATRIX SIGNAL
##########################################################################################
# Compute the correlation matrix for the signal
corr = sig[features + ['bdt', 'cand_refit_tau_mass']].corr()

# Set up the matplotlib figure
f, ax = plt.subplots(figsize=(11, 9))

# Generate a custom diverging colormap
cmap = sns.diverging_palette(220, 10, as_cmap=True)

# Draw the heatmap with the mask and correct aspect ratio
g = sns.heatmap(corr, cmap=cmap, vmax=1., vmin=-1, center=0, annot=True, fmt='.2f',
                square=True, linewidths=.8, cbar_kws={"shrink": .8})

# rotate axis labels
g.set_xticklabels(labels.values(), rotation='vertical')
g.set_yticklabels(labels.values(), rotation='horizontal')

# plt.show()
plt.title('linear correlation matrix - signal')
plt.tight_layout()
plt.savefig('corr_sig_%s.pdf' %tag)
plt.clf()

##########################################################################################
#####   CORRELATION MATRIX BACKGROUND
##########################################################################################
# Compute the correlation matrix for the signal
corr = bkg[features + ['bdt', 'cand_refit_tau_mass']].corr()

# Set up the matplotlib figure
f, ax = plt.subplots(figsize=(11, 9))

# Generate a custom diverging colormap
cmap = sns.diverging_palette(220, 10, as_cmap=True)

# Draw the heatmap with the mask and correct aspect ratio
g = sns.heatmap(corr, cmap=cmap, vmax=1., vmin=-1, center=0, annot=True, fmt='.2f',
                square=True, linewidths=.8, cbar_kws={"shrink": .8})

# rotate axis labels
g.set_xticklabels(labels.values(), rotation='vertical')
g.set_yticklabels(labels.values(), rotation='horizontal')

# plt.show()
plt.title('linear correlation matrix - background')
plt.tight_layout()
plt.savefig('corr_bkg_%s.pdf' %tag)
