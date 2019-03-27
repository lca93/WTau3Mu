#!/bin/bash

#data="/eos/user/m/manzoni/WTau3Mu/ntuples_16_4_2018/data_enriched_16apr2018v16.root"
#mc="/eos/user/m/manzoni/WTau3Mu/ntuples_16_4_2018/signal_enriched_16apr2018v16.root"

data="data_enriched_16apr2018_v16_skimmed.root"
mc="signal_enriched_16apr2018_v16.root"
wps='0.60 0.61 0.62 0.63 0.64 0.65 0.66 0.67 0.68 0.69 0.70 0.71 0.72 0.73 0.74 0.75 0.76 0.77 0.78 0.79 0.80 0.81 0.82 0.83 0.84 0.85 0.86 0.87 0.88 0.89 0.90 0.91 0.92 0.93 0.94'
# wps='0.84 0.89'
# wps='0.89'
# wps='0.6'

# phi veto
baseline="( ((abs(cand_refit_mass12-1.020)<0.02)*(cand_charge12==0)) + ((abs(cand_refit_mass13-1.020)<0.02)*(cand_charge13==0)) + ((abs(cand_refit_mass23-1.020)<0.02)*(cand_charge23==0)) )==0"
# omega veto
baseline+=' & ( ((abs(cand_refit_mass12-0.782)<0.02)*(cand_charge12==0)) + ((abs(cand_refit_mass13-0.782)<0.02)*(cand_charge13==0)) + ((abs(cand_refit_mass23-0.782)<0.02)*(cand_charge23==0)) )==0'
# 3mu charge and mass window
baseline+=' & abs(cand_charge)==1 & abs(cand_refit_tau_mass-1.8)<0.2'
# HLT dimuon mass cut override
baseline+='& ((mu1_hlt_doublemu3_trk_tau3mu_type==83 & mu2_hlt_doublemu3_trk_tau3mu_type==83 & cand_mass12>0.5 & cand_mass12<1.7) |'
baseline+='   (mu1_hlt_doublemu3_trk_tau3mu_type==83 & mu3_hlt_doublemu3_trk_tau3mu_type==83 & cand_mass13>0.5 & cand_mass13<1.7) |'
baseline+='   (mu2_hlt_doublemu3_trk_tau3mu_type==83 & mu3_hlt_doublemu3_trk_tau3mu_type==83 & cand_mass23>0.5 & cand_mass23<1.7) )'


for wp in $wps
    do
    selection="bdt>$wp & $baseline"
    echo 'Selection'
    echo $selection
    barrel_selection="$selection & abs(cand_refit_tau_eta)< 1.6"
    endcap_selection="$selection & abs(cand_refit_tau_eta)>=1.6"
#     echo $barrel_selection
#     echo $endcap_selection

    ######################################################################################
    ./prepare_cards_v3.py --selection="$barrel_selection" --category='barrel'$wp --datafile=$data --sigfile=$mc --blinded
    ./prepare_cards_v3.py --selection="$endcap_selection" --category='endcap'$wp --datafile=$data --sigfile=$mc --blinded
    ######################################################################################

    done
