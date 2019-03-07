import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from itertools import product
from root_numpy import root2array
from sklearn.metrics import roc_curve, roc_auc_score

# rather irrelevant fiddling with figure and text size
font = {'family' : 'normal',
        'weight' : 'normal',
        'size'   : 22}
matplotlib.rc('font', **font)
matplotlib.rcParams['figure.figsize'] = [15, 10] ; 

# define the branches we need to convert from ROOT to pandas
branches = [
    'cand_refit_tau_mass'              ,
    'bdt'                              ,
    'cand_charge'                      ,
    'mcweight'                         ,
    'cand_refit_tau_eta'               ,
    'cand_refit_mass12'                ,
    'cand_refit_mass13'                ,
    'cand_refit_mass23'                ,
    'cand_mass12'                      ,
    'cand_mass13'                      ,
    'cand_mass23'                      ,
    'cand_charge12'                    ,
    'cand_charge13'                    ,
    'cand_charge23'                    ,
    'mu1_hlt_doublemu3_trk_tau3mu_type',
    'mu2_hlt_doublemu3_trk_tau3mu_type',
    'mu3_hlt_doublemu3_trk_tau3mu_type',
]

# tag = '16apr2018_v16'
tag = '5mar2019_v4'

sig_file_name = '/Users/manzoni/Documents/tau3mu2018/5mar2019/ntuples/signal_enriched_%s.root' %tag
bkg_file_name = '/Users/manzoni/Documents/tau3mu2018/5mar2019/ntuples/data_enriched_%s.root' %tag

preselection = '( ((abs(cand_refit_mass12-1.020)<0.02)*(cand_charge12==0)) + ((abs(cand_refit_mass13-1.020)<0.02)*(cand_charge13==0)) + ((abs(cand_refit_mass23-1.020)<0.02)*(cand_charge23==0)) )==0 & ( ((abs(cand_refit_mass12-0.782)<0.02)*(cand_charge12==0)) + ((abs(cand_refit_mass13-0.782)<0.02)*(cand_charge13==0)) + ((abs(cand_refit_mass23-0.782)<0.02)*(cand_charge23==0)) )==0 & abs(cand_charge)==1 & abs(cand_refit_tau_mass-1.8)<0.2& ((mu1_hlt_doublemu3_trk_tau3mu_type==83 & mu2_hlt_doublemu3_trk_tau3mu_type==83 & cand_mass12>0.5 & cand_mass12<1.7) | (mu1_hlt_doublemu3_trk_tau3mu_type==83 & mu3_hlt_doublemu3_trk_tau3mu_type==83 & cand_mass13>0.5 & cand_mass13<1.7) | (mu2_hlt_doublemu3_trk_tau3mu_type==83 & mu3_hlt_doublemu3_trk_tau3mu_type==83 & cand_mass23>0.5 & cand_mass23<1.7) )'

# convert root trees into pandas datasets.
# Use the buil-in doc to know more about the funtions used here
# apply some very loose isolation selection for consistency
sig = pd.DataFrame( root2array(sig_file_name, 'tree', branches = branches, selection = preselection                                         ) ) # genuine, hadronically decaying taus
bkg = pd.DataFrame( root2array(bkg_file_name, 'tree', branches = branches, selection = preselection + '& abs(cand_refit_tau_mass-1.78)>0.06') ) # jets faking taus

# define targets: genuine taus get 1, fake taus get 0
sig['target'] = np.ones (sig.shape[0]).astype(np.int)
bkg['target'] = np.zeros(bkg.shape[0]).astype(np.int)

# concatenate the datasets, preserving the information
alltaus = pd.concat([sig, bkg])

# let sklearn do the heavy lifting and compute the ROC curves for you
fpr_mva, tpr_mva, wps_mva = roc_curve(alltaus.target, alltaus.bdt) 

# plot
plt.plot(fpr_mva, tpr_mva, label='BDT', color='b')

############################################################################################

# plot the also the diagonal, that corresponds to no random picks, no discrimination power
xy = [i*j for i,j in product([10.**i for i in range(-8, 0)], [1,2,4,8])]+[1]
plt.plot(xy, xy, color='grey', linestyle='--')

# cosmetics
plt.xlabel(r'data sidebands fake rate') # aka 'False Positive Rate' outside hep
plt.ylabel(r'signal $\tau\to3\mu$ efficiency') # aka 'True Positive Rate' outside hep

# axis range
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.0])

# log scale
plt.xlim([1.e-6, 1.0])
plt.xscale('log')

# grid
plt.grid(True)

# legend
plt.legend(loc='lower right')

# if on gridui, save the figure
# plt.savefig('roc_curve_16apr2018_v16.pdf')
plt.savefig('roc_curve_5mar2019_v4.pdf')
