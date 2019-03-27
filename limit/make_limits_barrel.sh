#! /bin/bash

wps='0.60 0.61 0.62 0.63 0.64 0.65 0.66 0.67 0.68 0.69 0.70 0.71 0.72 0.73 0.74 0.75 0.76 0.77 0.78 0.79 0.80 0.81 0.82 0.83 0.84 0.85 0.86 0.87 0.88 0.89 0.90 0.91 0.92 0.93 0.94'
# wps='0.80 0.81 0.82 0.83 0.84 0.85 0.86 0.87 0.88 0.89 0.90'
# wps='0.89'
for wp in $wps
    do
    echo "WP "$wp
    echo "Running on barrel!"
    barrel='datacard_barrel'$wp'.txt'
    model='model_barrel'$wp'.root'

    echo "creating model"
    text2workspace.py $barrel -o $model 
    
    echo 'computing the 90% limit'
#     combine -M Asymptotic -t -1 -C 0.90 $barrel > "limit_barrel_CL_0p90_central_WP_b$wp.txt"

    combine -M HybridNew --testStat=LHC --frequentist $model -T 3000 --expectedFromGrid 0.500 -C 0.9  --plot=limit_barrel_hybridnew_scan_central_0.90_WP_b$wp.png         --rMin 0 --rMax 50  | grep Limit >  limit_barrel_hybridnew_CL_0p90_central_WP_b$wp.txt
    
    
    
    
    
    
    
    
#     combine -M HybridNew --testStat=LHC --frequentist $model -T 3000 --expectedFromGrid 0.978 -C 0.9  --plot=limit_scan_plus_two_sigma_0.90_WP_b0p89.png  --rMin 0 --rMax 50 > limit_barrel_CL_0p90_plus_two_sigma_WP_b0p89.txt
#     combine -M HybridNew --testStat=LHC --frequentist $model -T 3000 --expectedFromGrid 0.841 -C 0.9  --plot=limit_scan_plus_one_sigma_0.90_WP_b0p89.png  --rMin 0 --rMax 50 > limit_barrel_CL_0p90_plus_one_sigma_WP_b0p89.txt
#     combine -M HybridNew --testStat=LHC --frequentist $model -T 3000 --expectedFromGrid 0.500 -C 0.9  --plot=limit_scan_central_0.90_WP_b0p89.png         --rMin 0 --rMax 50  | grep Limit >  limit_barrel_CL_0p90_central_WP_b0p89.txt
#     combine -M HybridNew --testStat=LHC --frequentist $model -T 3000 --expectedFromGrid 0.159 -C 0.9  --plot=limit_scan_minus_one_sigma_0.90_WP_b0p89.png --rMin 0 --rMax 50 > limit_barrel_CL_0p90_minus_one_sigma_WP_b0p89.txt
#     combine -M HybridNew --testStat=LHC --frequentist $model -T 3000 --expectedFromGrid 0.022 -C 0.9  --plot=limit_scan_minus_two_sigma_0.90_WP_b0p89.png --rMin 0 --rMax 50 > limit_barrel_CL_0p90_minus_two_sigma_WP_b0p89.txt
# 
#     combine -M HybridNew --testStat=LHC --frequentist $model -T 3000 --expectedFromGrid 0.978 -C 0.95 --plot=limit_scan_plus_two_sigma_0.95_WP_b0p89.png  --rMin 0 --rMax 50 > limit_barrel_CL_0p95_plus_two_sigma_WP_b0p89.txt
#     combine -M HybridNew --testStat=LHC --frequentist $model -T 3000 --expectedFromGrid 0.841 -C 0.95 --plot=limit_scan_plus_one_sigma_0.95_WP_b0p89.png  --rMin 0 --rMax 50 > limit_barrel_CL_0p95_plus_one_sigma_WP_b0p89.txt
#     combine -M HybridNew --testStat=LHC --frequentist $model -T 3000 --expectedFromGrid 0.500 -C 0.95 --plot=limit_scan_central_0.95_WP_b0p89.png         --rMin 0 --rMax 50 > limit_barrel_CL_0p95_central_WP_b0p89.txt
#     combine -M HybridNew --testStat=LHC --frequentist $model -T 3000 --expectedFromGrid 0.159 -C 0.95 --plot=limit_scan_minus_one_sigma_0.95_WP_b0p89.png --rMin 0 --rMax 50 > limit_barrel_CL_0p95_minus_one_sigma_WP_b0p89.txt
#     combine -M HybridNew --testStat=LHC --frequentist $model -T 3000 --expectedFromGrid 0.022 -C 0.95 --plot=limit_scan_minus_two_sigma_0.95_WP_b0p89.png --rMin 0 --rMax 50 > limit_barrel_CL_0p95_minus_two_sigma_WP_b0p89.txt

#     combine -M HybridNew --testStat=LHC --frequentist $model -T 1000 --expectedFromGrid 0.5  -C 0.9 --plot=limit_scan_central_0.90_WP$wp.png --rMin 0 --rMax 10 > barrel_central_0.90_WP$wp.txt
#     combine -M HybridNew --testStat=LHC --frequentist $model -T 1000 --expectedFromGrid 0.16 -C 0.9 --plot=limit_scan_minus_0.90_WP$wp.png   --rMin 0 --rMax 10 > barrel_minus_one_sigma_0.90_WP$wp.txt
#     combine -M HybridNew --testStat=LHC --frequentist $model -T 1000 --expectedFromGrid 0.84 -C 0.9 --plot=limit_scan_plus_0.90_WP$wp.png    --rMin 0 --rMax 10 > barrel_plus_one_sigma_0.90_WP$wp.txt

    # echo 'computing the 95% limit'
    # combine -M HybridNew --testStat=LHC --frequentist $model -T 3000 --expectedFromGrid 0.5  --plot=limit_scan_central_0.95_WP$wp.png --rMin 0 --rMax 8 > central_0.95_WP$wp.txt
    # combine -M HybridNew --testStat=LHC --frequentist $model -T 3000 --expectedFromGrid 0.16 --plot=limit_scan_minus_0.95_WP$wp.png   --rMin 0 --rMax 8 > plus_one_sigma_0.95_WP$wp.txt
    # combine -M HybridNew --testStat=LHC --frequentist $model -T 3000 --expectedFromGrid 0.84 --plot=limit_scan_plus_0.95_WP$wp.png    --rMin 0 --rMax 8 > minus_one_sigma_0.95_WP$wp.txt
    
    done



# combine central_0.90_WP0.89.txt -M HybridNew --LHCmode LHC-limits


#     combine -M HybridNew --testStat=LHC --frequentist model0.89.root -T 2000 --expectedFromGrid 0.5  -C 0.9 --plot=limit_scan.png --rMin=0 --rMax=4 &> central_0.90_WP_test.txt



# ombine -M HybridNew --testStat=LHC --frequentist model0.89.root -T 6000 --expectedFromGrid 0.5 -C 0.9 --rMin 1 --rMax 8




# combine -M HybridNew --testStat=LHC model0.89.root -T 100 --expectedFromGrid 0.5 -C 0.9  --rMin 0 --rMax 8
