#!/bin/bash

declare -a net_mdl_arr=("ws_k-10_p-0.10" "er_p-0.02" "sb_blocks-5_wip-0.05_bwp-0.01" "ba_m-5")

for net_mdl in "${net_mdl_arr[@]}"
do
    echo "$net_mdl"
    python3 -m plotting.make_scatter_input --data-dir 'data' --net-mdl-saved $net_mdl \
        --n 500 --tau 0.4 --n-iters 100 \
        --expo-mdl-name 'frac-nbr-expo' --q 0.5 \
        --rand-mdl-name 'complete' --n-z 100000 --n-cutoff 1000 \

    python3 -m plotting.make_scatter_input --data-dir 'data' --net-mdl-saved $net_mdl \
        --n 500 --tau 0.4 --n-iters 100 \
        --expo-mdl-name 'frac-nbr-expo' --q 0.5 \
        --rand-mdl-name 'restricted' --n-z 100000 --n-cutoff 1000 \
        --fitness-fn-name 'square-smd_frac-expo' --smd-weight 1.0 --expo-weight 1.0 \

    python3 -m plotting.make_scatter_input --data-dir 'data' --net-mdl-saved $net_mdl \
        --n 500 --tau 0.4 --n-iters 100 \
        --expo-mdl-name 'frac-nbr-expo' --q 0.5 \
        --rand-mdl-name 'restricted-genetic' --n-z 10000 --n-cutoff 1000 \
        --fitness-fn-name 'square-smd_frac-expo' --smd-weight 1.0 --expo-weight 1.0 \

    python3 -m plotting.make_scatter_input --data-dir 'data' --net-mdl-saved $net_mdl \
        --n 500 --tau 0.4 --n-iters 100 \
        --expo-mdl-name 'frac-nbr-expo' --q 0.5 \
        --rand-mdl-name 'graph' --n-z 10000 --n-cutoff 1000 \

    python3 -m plotting.plot_scatter --net-mdl-saved $net_mdl
done