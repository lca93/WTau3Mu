import os
import re
import ROOT
import numpy as np
from itertools import product

ROOT.gStyle.SetOptStat(False)
ROOT.gStyle.SetPaintTextFormat('4.2f')

# wps='0.60 0.61 0.62 0.63 0.64 0.65 0.66 0.67 0.68 0.69 0.70 0.71 0.72 0.73 0.74 0.75 0.76 0.77 0.78 0.79 0.80 0.81 0.82 0.83 0.84 0.85 0.86 0.87 0.88 0.89 0.90 0.91 0.92 0.93 0.94'
# wpsb='0.80 0.81 0.82 0.83 0.84 0.85 0.86 0.87 0.88 0.89 0.90 0.91 0.92'
wpsb = np.array([0.85, 0.86, 0.87, 0.88, 0.89, 0.90, 0.91]) #, 0.92])
wpse = np.array([0.70, 0.72, 0.74, 0.76, 0.78, 0.80, 0.82, 0.84, 0.86, 0.88, 0.90])

c1 = ROOT.TCanvas('c1', '', 1000, 1000)

limits = ROOT.TH2F('limits', '', len(wpsb)-1, wpsb, len(wpse)-1, wpse)
limits.GetXaxis().SetTitle('BDT cut for barrel (|#eta_{#tau}|<1.6)')
limits.GetYaxis().SetTitle('BDT cut for endcap (|#eta_{#tau}|>1.6)')
limits.GetZaxis().SetTitle('expected limit @90% CL [10^{-7}]')
limits.GetZaxis().SetRangeUser(1., 2.)

limit_file_name = 'limit_combined_hybridnew_CL_0p90_central_WP_bBWP_eEWP.txt'

for bwp, ewp in product(wpsb, wpse):

    toopen = limit_file_name.replace('BWP', '%.2f'%bwp).replace('EWP', '%.2f'%ewp)

    file = open(toopen)
    lines = file.readlines(0)
    if len(lines) != 1:
        continue
    line = lines[0]
    value, error = re.findall(r"\d+\.\d+", line)
    value, error = float(value), float(error) 
    limits.Fill(bwp, ewp, value)
    ibinx = sum(wpsb<bwp)
    ibiny = sum(wpse<ewp)
    limits.SetBinError(ibinx, ibiny, error)
    
limits.Draw('colz text e')

# ROOT.gPad.SetTopMargin   (0.15)
ROOT.gPad.SetBottomMargin(0.15)
ROOT.gPad.SetLeftMargin  (0.15)
ROOT.gPad.SetRightMargin (0.15)

limits.GetXaxis().SetTitleOffset(1.3)
limits.GetYaxis().SetTitleOffset(1.3)
limits.GetZaxis().SetTitleOffset(1.3)

ROOT.gPad.Update()

ROOT.gPad.SaveAs('bdt_optimisation_veto_omega_phi_trigger.pdf')

