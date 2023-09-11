#!/bin/bash

declare -a net_mdl_arr=("ws_k-10_p-0.10" "er_p-0.02" "sb_blocks-5_wip-0.05_bwp-0.01" "ba_m-5")
n=500
n_iters=100

for net_mdl in "${net_mdl_arr[@]}"
do
    python3 -m utils.check_graph_clusters --data-dir 'data' --net-mdl-saved $net_mdl \
        --n $n --n-iters $n_iters \
        --rand-mdl-name 'graph'
done