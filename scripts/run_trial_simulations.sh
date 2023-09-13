#!/bin/bash

declare -a net_mdl_arr=("ws_k-10_p-0.10" "er_p-0.02" "sb_blocks-5_wip-0.05_bwp-0.01" "ba_m-5")

for net_mdl in "${net_mdl_arr[@]}"
do
    for n in 100 500
    do  
        python3 -m simulate_trial --data-dir 'data' --net-mdl-saved $net_mdl \
            --n $n --n-iters 500 --tau 0.0 \
            --expo-mdl-name 'one-nbr-expo' \
            --outcome-mdl-name 'additive' --delta-size 0.0 \
            --rand-mdl-name 'complete' --n-z 1000 --n-cutoff 1000 \
            --est-name 'diff-in-means'

        python3 -m simulate_trial --data-dir 'data' --net-mdl-saved $net_mdl \
            --n $n --n-iters 500 --tau 0.0 \
            --expo-mdl-name 'one-nbr-expo' \
            --outcome-mdl-name 'additive' --delta-size 0.0 \
            --rand-mdl-name 'restricted' --n-z 100000 --n-cutoff 1000 \
            --fitness-fn-name 'square-smd_frac-expo' --smd-weight 1.0 --expo-weight 1.0 \
            --est-name 'diff-in-means'
        
        # python3 -m simulate_trial --data-dir 'data' --net-mdl-saved $net_mdl \
        #     --n $n --n-iters 500 --tau 0.0 \
        #     --expo-mdl-name 'one-nbr-expo' \
        #     --outcome-mdl-name 'additive' --delta-size 0.0 \
        #     --rand-mdl-name 'restricted' --n-z 100000 --n-cutoff 1000 \
        #     --fitness-fn-name 'bias-term' \
        #     --est-name 'diff-in-means'

        python3 -m simulate_trial --data-dir 'data' --net-mdl-saved $net_mdl \
            --n $n --n-iters 500 --tau 0.0 \
            --expo-mdl-name 'one-nbr-expo' \
            --outcome-mdl-name 'additive' --delta-size 0.0 \
            --rand-mdl-name 'restricted-genetic' --n-z 10000 --n-cutoff 1000 \
            --fitness-fn-name 'square-smd_frac-expo' --smd-weight 1.0 --expo-weight 1.0 \
            --est-name 'diff-in-means'

        # python3 -m simulate_trial --data-dir 'data' --net-mdl-saved $net_mdl \
        #     --n $n --n-iters 500 --tau 0.0 \
        #     --expo-mdl-name 'one-nbr-expo' \
        #     --outcome-mdl-name 'additive' --delta-size 0.0 \
        #     --rand-mdl-name 'restricted-genetic' --n-z 10000 --n-cutoff 1000 \
        #     --fitness-fn-name 'bias-term' \
        #     --est-name 'diff-in-means'

        python3 -m simulate_trial --data-dir 'data' --net-mdl-saved $net_mdl \
            --n $n --n-iters 500 --tau 0.0 \
            --expo-mdl-name 'one-nbr-expo' \
            --outcome-mdl-name 'additive' --delta-size 0.0 \
            --rand-mdl-name 'graph' --n-z 1000 --n-cutoff 1000 \
            --est-name 'diff-in-means'

        python3 -m simulate_trial --data-dir 'data' --net-mdl-saved $net_mdl \
            --n $n --n-iters 500 --tau 0.0 \
            --expo-mdl-name 'one-nbr-expo' \
            --outcome-mdl-name 'additive' --delta-size 0.0 \
            --rand-mdl-name 'graph-restricted' --n-z 10000 --n-cutoff 1000 \
            --fitness-fn-name 'square-smd_frac-expo' --smd-weight 1.0 --expo-weight 1.0 \
            --est-name 'diff-in-means'

        python3 -m simulate_trial --data-dir 'data' --net-mdl-saved $net_mdl \
            --n $n --n-iters 500 --tau 0.0 \
            --expo-mdl-name 'one-nbr-expo' \
            --outcome-mdl-name 'additive' --delta-size 0.0 \
            --rand-mdl-name 'graph-restricted-genetic' --n-z 10000 --n-cutoff 1000 \
            --fitness-fn-name 'square-smd_frac-expo' --smd-weight 1.0 --expo-weight 1.0 \
            --est-name 'diff-in-means'

        for tau in 0.4 0.8 
        do
            python3 -m simulate_trial --data-dir 'data' --net-mdl-saved $net_mdl \
                --n $n --n-iters 500 --tau $tau \
                --expo-mdl-name 'frac-nbr-expo' --q 0.25 0.50 0.75 \
                --outcome-mdl-name 'additive' --delta-size 0.5 \
                --rand-mdl-name 'complete' --n-z 1000 --n-cutoff 1000 \
                --est-name 'diff-in-means'

            python3 -m simulate_trial --data-dir 'data' --net-mdl-saved $net_mdl \
                --n $n --n-iters 500 --tau $tau \
                --expo-mdl-name 'frac-nbr-expo' --q 0.25 0.50 0.75 \
                --outcome-mdl-name 'additive' --delta-size 0.5 \
                --rand-mdl-name 'restricted' --n-z 100000 --n-cutoff 1000 \
                --fitness-fn-name 'square-smd_frac-expo' --smd-weight 1.0 --expo-weight 1.0 \
                --est-name 'diff-in-means'

            python3 -m simulate_trial --data-dir 'data' --net-mdl-saved $net_mdl \
                --n $n --n-iters 500 --tau $tau \
                --expo-mdl-name 'frac-nbr-expo' --q 0.25 0.50 0.75 \
                --outcome-mdl-name 'additive' --delta-size 0.5 \
                --rand-mdl-name 'restricted-genetic' --n-z 10000 --n-cutoff 1000 \
                --fitness-fn-name 'square-smd_frac-expo' --smd-weight 1.0 --expo-weight 1.0 \
                --est-name 'diff-in-means'

            python3 -m simulate_trial --data-dir 'data' --net-mdl-saved $net_mdl \
                --n $n --n-iters 500 --tau $tau \
                --expo-mdl-name 'frac-nbr-expo' --q 0.25 0.50 0.75 \
                --outcome-mdl-name 'additive' --delta-size 0.5 \
                --rand-mdl-name 'graph' --n-z 1000 --n-cutoff 1000 \
                --est-name 'diff-in-means'

            python3 -m simulate_trial --data-dir 'data' --net-mdl-saved $net_mdl \
                --n $n --n-iters 500 --tau $tau \
                --expo-mdl-name 'frac-nbr-expo' --q 0.25 0.50 0.75 \
                --outcome-mdl-name 'additive' --delta-size 0.5 \
                --rand-mdl-name 'graph-restricted' --n-z 10000 --n-cutoff 1000 \
                --fitness-fn-name 'square-smd_frac-expo' --smd-weight 1.0 --expo-weight 1.0 \
                --est-name 'diff-in-means'

            python3 -m simulate_trial --data-dir 'data' --net-mdl-saved $net_mdl \
                --n $n --n-iters 500 --tau $tau \
                --expo-mdl-name 'frac-nbr-expo' --q 0.25 0.50 0.75 \
                --outcome-mdl-name 'additive' --delta-size 0.5 \
                --rand-mdl-name 'graph-restricted-genetic' --n-z 10000 --n-cutoff 1000 \
                --fitness-fn-name 'square-smd_frac-expo' --smd-weight 1.0 --expo-weight 1.0 \
                --est-name 'diff-in-means'
        done
    done
done