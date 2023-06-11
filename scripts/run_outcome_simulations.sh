#!/bin/bash

declare -a net_mdl_arr=("ws_k-10_p-0.10" "er_p-0.02" "sb_blocks-5_wip-0.05_bwp-0.01" "ba_m-5")

for net in "${net_mdl_arr[@]}"
do
    for n in 100 500 
    do 
        for tau in 0.0 0.4 0.8
        do
            for n_iters in 100 500 1000 
            do 
                python3 -m simulate_outcomes --n $n --tau $tau --net-mdl-saved $net --n-iters $n_iters
            done
        done
    done
done
