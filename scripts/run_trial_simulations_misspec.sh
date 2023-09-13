#!/bin/bash

declare -a net_mdl_arr=("ws_k-10_p-0.10" "er_p-0.02" "sb_blocks-5_wip-0.05_bwp-0.01" "ba_m-5")
n=500
tau=0.4

for net_mdl in "${net_mdl_arr[@]}"
do
    python3 -m simulate_trial_misspec --data-dir 'data' --net-mdl-saved $net_mdl \
        --n $n --n-iters 500 --tau $tau \
        --expo-mdl-name 'frac-nbr-expo' --q 0.50 \
        --outcome-mdl-name 'additive' --delta-size 0.5 \
        --rand-mdl-name 'restricted' --n-z 100000 --n-cutoff 1000 \
        --fitness-fn-name 'square-smd_frac-expo' --smd-weight 1.0 --expo-weight 1.0 \
        --est-name 'diff-in-means' \
        --misspec-type 'add-remove' --p-add 0.01 0.05 0.1 0.5 --p-remove 0.01 0.05 0.1 0.5

    python3 -m simulate_trial_misspec --data-dir 'data' --net-mdl-saved $net_mdl \
        --n $n --n-iters 500 --tau $tau \
        --expo-mdl-name 'frac-nbr-expo' --q 0.50 \
        --outcome-mdl-name 'additive' --delta-size 0.5 \
        --rand-mdl-name 'restricted-genetic' --n-z 10000 --n-cutoff 1000 \
        --fitness-fn-name 'square-smd_frac-expo' --smd-weight 1.0 --expo-weight 1.0 \
        --est-name 'diff-in-means' \
        --misspec-type 'add-remove' --p-add 0.01 0.05 0.1 0.5 --p-remove 0.01 0.05 0.1 0.5

    python3 -m simulate_trial_misspec --data-dir 'data' --net-mdl-saved $net_mdl \
        --n $n --n-iters 500 --tau $tau \
        --expo-mdl-name 'frac-nbr-expo' --q 0.50 \
        --outcome-mdl-name 'additive' --delta-size 0.5 \
        --rand-mdl-name 'graph' --n-z 1000 --n-cutoff 1000 \
        --est-name 'diff-in-means' \
        --misspec-type 'add-remove' --p-add 0.01 0.05 0.1 0.5 --p-remove 0.01 0.05 0.1 0.5

    python3 -m simulate_trial_misspec --data-dir 'data' --net-mdl-saved $net_mdl \
        --n $n --n-iters 500 --tau $tau \
        --expo-mdl-name 'frac-nbr-expo' --q 0.50 \
        --outcome-mdl-name 'additive' --delta-size 0.5 \
        --rand-mdl-name 'graph-restricted' --n-z 10000 --n-cutoff 1000 \
        --fitness-fn-name 'square-smd_frac-expo' --smd-weight 1.0 --expo-weight 1.0 \
        --est-name 'diff-in-means' \
        --misspec-type 'add-remove' --p-add 0.01 0.05 0.1 0.5 --p-remove 0.01 0.05 0.1 0.5

    python3 -m simulate_trial_misspec --data-dir 'data' --net-mdl-saved $net_mdl \
        --n $n --n-iters 500 --tau $tau \
        --expo-mdl-name 'frac-nbr-expo' --q 0.50 \
        --outcome-mdl-name 'additive' --delta-size 0.5 \
        --rand-mdl-name 'graph-restricted-genetic' --n-z 10000 --n-cutoff 1000 \
        --fitness-fn-name 'square-smd_frac-expo' --smd-weight 1.0 --expo-weight 1.0 \
        --est-name 'diff-in-means' \
        --misspec-type 'add-remove' --p-add 0.01 0.05 0.1 0.5 --p-remove 0.01 0.05 0.1 0.5
done