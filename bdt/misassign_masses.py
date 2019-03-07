import ROOT
import root_pandas
import numpy as np
import pandas
import root_numpy

global m_k
global m_pi

m_k  = 0.493677
m_pi = 0.13957061

# tree = ROOT.TChain('tree')
# tree.Add('/Users/manzoni/Documents/tau3mu2018/16april/ntuples/data_enriched_16apr2018v16.root')

print 'loading dataset...'
dataset = pandas.DataFrame(root_numpy.root2array(
    '/Users/manzoni/Documents/tau3mu2018/16april/ntuples/data_enriched_16apr2018v16.root', 
    'tree', 
#     start=0, 
#     stop=100000,
    )
)
print '\t...done'

mpp12_array = []
mpp13_array = []
mpp23_array = []

mkk12_array = []
mkk13_array = []
mkk23_array = []

mkp12_array = []
mkp13_array = []
mkp23_array = []

mpk12_array = []
mpk13_array = []
mpk23_array = []

mppp_array  = []
mppk_array  = []
mpkp_array  = []
mkpp_array  = []
mpkk_array  = []
mkpk_array  = []
mkkp_array  = []
mkkk_array  = []

# for i, ev in enumerate(tree):

for i in range(len(dataset)):
    if i%10000 == 0:
        print '========> processed %d/%d \tevents\t%.1f' %(i, len(dataset), float(i)/len(dataset))
# for i in range(10):
    
#     k1p4  = ROOT.Math.LorentzVector('ROOT::Math::PtEtaPhiM4D<double>')(ev.mu1_pt, ev.mu1_eta, ev.mu1_phi, m_k )
#     k2p4  = ROOT.Math.LorentzVector('ROOT::Math::PtEtaPhiM4D<double>')(ev.mu2_pt, ev.mu2_eta, ev.mu2_phi, m_k )
#     k3p4  = ROOT.Math.LorentzVector('ROOT::Math::PtEtaPhiM4D<double>')(ev.mu3_pt, ev.mu3_eta, ev.mu3_phi, m_k )
# 
#     pi1p4 = ROOT.Math.LorentzVector('ROOT::Math::PtEtaPhiM4D<double>')(ev.mu1_pt, ev.mu1_eta, ev.mu1_phi, m_pi)
#     pi2p4 = ROOT.Math.LorentzVector('ROOT::Math::PtEtaPhiM4D<double>')(ev.mu2_pt, ev.mu2_eta, ev.mu2_phi, m_pi)
#     pi3p4 = ROOT.Math.LorentzVector('ROOT::Math::PtEtaPhiM4D<double>')(ev.mu3_pt, ev.mu3_eta, ev.mu3_phi, m_pi)

    k1p4  = ROOT.Math.LorentzVector('ROOT::Math::PtEtaPhiM4D<double>')(dataset.mu1_refit_pt[i], dataset.mu1_refit_eta[i], dataset.mu1_refit_phi[i], m_k )
    k2p4  = ROOT.Math.LorentzVector('ROOT::Math::PtEtaPhiM4D<double>')(dataset.mu2_refit_pt[i], dataset.mu2_refit_eta[i], dataset.mu2_refit_phi[i], m_k )
    k3p4  = ROOT.Math.LorentzVector('ROOT::Math::PtEtaPhiM4D<double>')(dataset.mu3_refit_pt[i], dataset.mu3_refit_eta[i], dataset.mu3_refit_phi[i], m_k )

    pi1p4 = ROOT.Math.LorentzVector('ROOT::Math::PtEtaPhiM4D<double>')(dataset.mu1_refit_pt[i], dataset.mu1_refit_eta[i], dataset.mu1_refit_phi[i], m_pi)
    pi2p4 = ROOT.Math.LorentzVector('ROOT::Math::PtEtaPhiM4D<double>')(dataset.mu2_refit_pt[i], dataset.mu2_refit_eta[i], dataset.mu2_refit_phi[i], m_pi)
    pi3p4 = ROOT.Math.LorentzVector('ROOT::Math::PtEtaPhiM4D<double>')(dataset.mu3_refit_pt[i], dataset.mu3_refit_eta[i], dataset.mu3_refit_phi[i], m_pi)
    
    mpp12 = (pi1p4 + pi2p4).mass()
    mpp13 = (pi1p4 + pi3p4).mass()
    mpp23 = (pi2p4 + pi3p4).mass()
    
    mkk12 = (k1p4 + k2p4).mass()
    mkk13 = (k1p4 + k3p4).mass()
    mkk23 = (k2p4 + k3p4).mass()

    mkp12 = (k1p4 + pi2p4).mass()
    mkp13 = (k1p4 + pi3p4).mass()
    mkp23 = (k2p4 + pi3p4).mass()

    mpk12 = (pi1p4 + k2p4).mass()
    mpk13 = (pi1p4 + k3p4).mass()
    mpk23 = (pi2p4 + k3p4).mass()
    
    mppp  = (pi1p4 + pi2p4 + pi3p4).mass()
    mppk  = (pi1p4 + pi2p4 + k3p4 ).mass()
    mpkp  = (pi1p4 + k2p4  + pi3p4).mass()
    mkpp  = (k1p4  + pi2p4 + pi3p4).mass()
    mpkk  = (pi1p4 + k2p4  + k3p4 ).mass()
    mkpk  = (k1p4  + pi2p4 + k3p4 ).mass()
    mkkp  = (k1p4  + k2p4  + pi3p4).mass()
    mkkk  = (k1p4  + k2p4  + k3p4 ).mass()

    mpp12_array.append(mpp12)
    mpp13_array.append(mpp13)
    mpp23_array.append(mpp23)

    mkk12_array.append(mkk12)
    mkk13_array.append(mkk13)
    mkk23_array.append(mkk23)

    mkp12_array.append(mkp12)
    mkp13_array.append(mkp13)
    mkp23_array.append(mkp23)

    mpk12_array.append(mpk12)
    mpk13_array.append(mpk13)
    mpk23_array.append(mpk23)

    mppp_array .append(mppp )
    mppk_array .append(mppk )
    mpkp_array .append(mpkp )
    mkpp_array .append(mkpp )
    mpkk_array .append(mpkk )
    mkpk_array .append(mkpk )
    mkkp_array .append(mkkp )
    mkkk_array .append(mkkk )


dataset['mpp12'] = mpp12_array
dataset['mpp13'] = mpp13_array
dataset['mpp23'] = mpp23_array

dataset['mkk12'] = mkk12_array
dataset['mkk13'] = mkk13_array
dataset['mkk23'] = mkk23_array

dataset['mkp12'] = mkp12_array
dataset['mkp13'] = mkp13_array
dataset['mkp23'] = mkp23_array

dataset['mpk12'] = mpk12_array
dataset['mpk13'] = mpk13_array
dataset['mpk23'] = mpk23_array

dataset['mppp']  = mppp_array
dataset['mppk']  = mppk_array
dataset['mpkp']  = mpkp_array
dataset['mkpp']  = mkpp_array
dataset['mpkk']  = mpkk_array
dataset['mkpk']  = mkpk_array
dataset['mkkp']  = mkkp_array
dataset['mkkk']  = mkkk_array

print 'staging dataset...'
dataset.to_root(
    '/Users/manzoni/Documents/tau3mu2018/16april/ntuples/data_enriched_16apr2018v16_extra_masses.root', 
    key='tree', 
    store_index=False
)
print '\t...done'
