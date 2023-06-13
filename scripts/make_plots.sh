#!/bin/bash

declare -a net_mdl_arr=("ws_k-10_p-0.10" "er_p-0.02" "sb_blocks-5_wip-0.05_bwp-0.01" "ba_m-5")

for tau in 0.4 0.8
do
    for net_mdl in "${net_mdl_arr[@]}"
    do
        python3 -m plotting.make_plot_inputs --data-dir 'data' --net-mdl-saved $net_mdl \
                --n 500 --tau $tau --n-iters 100 \
                --expo-mdl-name 'one-nbr-expo' \
                --rand-mdl-name 'complete' --n-z 1000 --n-cutoff 1000 \
                --outcome-mdl-name 'additive' --delta-size 1.0 \
                --est-name 'diff-in-means'

        python3 -m plotting.make_plot_inputs --data-dir 'data' --net-mdl-saved $net_mdl \
            --n 500 --tau $tau --n-iters 100 \
            --expo-mdl-name 'one-nbr-expo' \
            --rand-mdl-name 'restricted' --n-z 100000 --n-cutoff 1000 \
            --fitness-fn-name 'square-smd_frac-expo' --smd-weight 1.0 --expo-weight 1.0 \
            --outcome-mdl-name 'additive' --delta-size 1.0 \
            --est-name 'diff-in-means'

        python3 -m plotting.make_plot_inputs --data-dir 'data' --net-mdl-saved $net_mdl \
            --n 500 --tau $tau --n-iters 100 \
            --expo-mdl-name 'one-nbr-expo' \
            --rand-mdl-name 'restricted-genetic' --n-z 10000 --n-cutoff 1000 \
            --fitness-fn-name 'square-smd_frac-expo' --smd-weight 1.0 --expo-weight 1.0 \
            --outcome-mdl-name 'additive' --delta-size 1.0 \
            --est-name 'diff-in-means'

        python3 -m plotting.make_plot_inputs --data-dir 'data' --net-mdl-saved $net_mdl \
            --n 500 --tau $tau --n-iters 100 \
            --expo-mdl-name 'one-nbr-expo' \
            --rand-mdl-name 'graph' --n-z 10000 --n-cutoff 1000 \
            --outcome-mdl-name 'additive' --delta-size 1.0 \
            --est-name 'diff-in-means'

        python3 -m plotting.make_plots --net-mdl-saved $net_mdl --expo-mdl-name "one-nbr-expo" --tau 0.8

        for q in 0.25 0.50 0.75 1.00 
        do
            echo "$net_mdl"
            python3 -m plotting.make_plot_inputs --data-dir 'data' --net-mdl-saved $net_mdl \
                --n 500 --tau $tau --n-iters 100 \
                --expo-mdl-name 'frac-nbr-expo' --q $q \
                --rand-mdl-name 'complete' --n-z 1000 --n-cutoff 1000 \
                --outcome-mdl-name 'additive' --delta-size 1.0 \
                --est-name 'diff-in-means'

            python3 -m plotting.make_plot_inputs --data-dir 'data' --net-mdl-saved $net_mdl \
                --n 500 --tau $tau --n-iters 100 \
                --expo-mdl-name 'frac-nbr-expo' --q $q \
                --rand-mdl-name 'restricted' --n-z 100000 --n-cutoff 1000 \
                --fitness-fn-name 'square-smd_frac-expo' --smd-weight 1.0 --expo-weight 1.0 \
                --outcome-mdl-name 'additive' --delta-size 1.0 \
                --est-name 'diff-in-means'

            python3 -m plotting.make_plot_inputs --data-dir 'data' --net-mdl-saved $net_mdl \
                --n 500 --tau $tau --n-iters 100 \
                --expo-mdl-name 'frac-nbr-expo' --q $q \
                --rand-mdl-name 'restricted-genetic' --n-z 10000 --n-cutoff 1000 \
                --fitness-fn-name 'square-smd_frac-expo' --smd-weight 1.0 --expo-weight 1.0 \
                --outcome-mdl-name 'additive' --delta-size 1.0 \
                --est-name 'diff-in-means'

            python3 -m plotting.make_plot_inputs --data-dir 'data' --net-mdl-saved $net_mdl \
                --n 500 --tau $tau --n-iters 100 \
                --expo-mdl-name 'frac-nbr-expo' --q $q \
                --rand-mdl-name 'graph' --n-z 10000 --n-cutoff 1000 \
                --outcome-mdl-name 'additive' --delta-size 1.0 \
                --est-name 'diff-in-means'
            
            python3 -m plotting.make_plots --net-mdl-saved $net_mdl --expo-mdl-name "frac-nbr-expo-${q}" --tau 0.8
        done
    done
done

        