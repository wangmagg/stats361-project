#!/bin/bash

declare -a net_mdl_arr=("ws_k-10_p-0.10" "er_p-0.02" "sb_blocks-5_wip-0.05_bwp-0.01" "ba_m-5")
n=500
n_iters=100

for tau in 0.4 
do
    for net_mdl in "${net_mdl_arr[@]}"
    do  
        ################## ADD MISSPECIFICATION ####################
        python3 -m plotting.make_plot_inputs_misspec --data-dir 'data' --net-mdl-saved $net_mdl \
            --n $n --tau $tau --n-iters $n_iters \
            --expo-mdl-name 'one-nbr-expo' \
            --rand-mdl-name 'graph' --n-z 10000 --n-cutoff 1000 \
            --outcome-mdl-name 'additive' --delta-size 1.0 \
            --est-name 'diff-in-means' \
            --misspec-type 'add' --p-add 0.05 0.1 0.5

        python3 -m plotting.make_plot_inputs_misspec --data-dir 'data' --net-mdl-saved $net_mdl \
            --n $n --tau $tau --n-iters $n_iters \
            --expo-mdl-name 'one-nbr-expo' \
            --rand-mdl-name 'graph-restricted' --n-z 10000 --n-cutoff 1000 \
            --fitness-fn-name 'square-smd_frac-expo' --smd-weight 1.0 --expo-weight 1.0 \
            --outcome-mdl-name 'additive' --delta-size 1.0 \
            --est-name 'diff-in-means' \
            --misspec-type 'add' --p-add 0.05 0.1 0.5
        
        python3 -m plotting.make_plot_inputs_misspec --data-dir 'data' --net-mdl-saved $net_mdl \
            --n $n --tau $tau --n-iters $n_iters \
            --expo-mdl-name 'one-nbr-expo' \
            --rand-mdl-name 'graph-restricted-genetic' --n-z 10000 --n-cutoff 1000 \
            --fitness-fn-name 'square-smd_frac-expo' --smd-weight 1.0 --expo-weight 1.0 \
            --outcome-mdl-name 'additive' --delta-size 1.0 \
            --est-name 'diff-in-means' \
            --misspec-type 'add' --p-add 0.05 0.1 0.5

        python3 -m plotting.make_plot_inputs_misspec --data-dir 'data' --net-mdl-saved $net_mdl \
            --n $n --tau $tau --n-iters $n_iters \
            --expo-mdl-name 'one-nbr-expo' \
            --rand-mdl-name 'restricted' --n-z 100000 --n-cutoff 1000 \
            --fitness-fn-name 'square-smd_frac-expo' --smd-weight 1.0 --expo-weight 1.0 \
            --outcome-mdl-name 'additive' --delta-size 1.0 \
            --est-name 'diff-in-means' \
            --misspec-type 'add' --p-add 0.05 0.1 0.5

        python3 -m plotting.make_plot_inputs_misspec --data-dir 'data' --net-mdl-saved $net_mdl \
            --n $n --tau $tau --n-iters $n_iters \
            --expo-mdl-name 'one-nbr-expo' \
            --rand-mdl-name 'restricted-genetic' --n-z 10000 --n-cutoff 1000 \
            --fitness-fn-name 'square-smd_frac-expo' --smd-weight 1.0 --expo-weight 1.0 \
            --outcome-mdl-name 'additive' --delta-size 1.0 \
            --est-name 'diff-in-means' \
            --misspec-type 'add' --p-add 0.05 0.1 0.5

        python3 -m plotting.make_plots_misspec --n $n --n-iters $n_iters --net-mdl-saved $net_mdl --expo-mdl-name "one-nbr-expo" \
            --fitness-fn-name 'square-smd-1.00_frac-exposed-1.00' --tau $tau --misspec-type 'add' --p-add 0.05 0.1 0.5

        for q in 0.50
        do
            python3 -m plotting.make_plot_inputs_misspec --data-dir 'data' --net-mdl-saved $net_mdl \
                --n $n --tau $tau --n-iters $n_iters \
                --expo-mdl-name 'frac-nbr-expo' --q $q \
                --rand-mdl-name 'graph' --n-z 10000 --n-cutoff 1000 \
                --outcome-mdl-name 'additive' --delta-size 1.0 \
                --est-name 'diff-in-means' \
                --misspec-type 'add' --p-add 0.05 0.1 0.5

            python3 -m plotting.make_plot_inputs_misspec --data-dir 'data' --net-mdl-saved $net_mdl \
                --n $n --tau $tau --n-iters $n_iters \
                --expo-mdl-name 'frac-nbr-expo' --q $q \
                --rand-mdl-name 'graph-restricted' --n-z 10000 --n-cutoff 1000 \
                --fitness-fn-name 'square-smd_frac-expo' --smd-weight 1.0 --expo-weight 1.0 \
                --outcome-mdl-name 'additive' --delta-size 1.0 \
                --est-name 'diff-in-means' \
                --misspec-type 'add' --p-add 0.05 0.1 0.5

            python3 -m plotting.make_plot_inputs_misspec --data-dir 'data' --net-mdl-saved $net_mdl \
                --n $n --tau $tau --n-iters $n_iters \
                --expo-mdl-name 'frac-nbr-expo' --q $q \
                --rand-mdl-name 'graph-restricted-genetic' --n-z 10000 --n-cutoff 1000 \
                --fitness-fn-name 'square-smd_frac-expo' --smd-weight 1.0 --expo-weight 1.0 \
                --outcome-mdl-name 'additive' --delta-size 1.0 \
                --est-name 'diff-in-means' \
                --misspec-type 'add' --p-add 0.05 0.1 0.5

            python3 -m plotting.make_plot_inputs_misspec --data-dir 'data' --net-mdl-saved $net_mdl \
                --n $n --tau $tau --n-iters $n_iters \
                --expo-mdl-name 'frac-nbr-expo' --q $q \
                --rand-mdl-name 'restricted' --n-z 100000 --n-cutoff 1000 \
                --fitness-fn-name 'square-smd_frac-expo' --smd-weight 1.0 --expo-weight 1.0 \
                --outcome-mdl-name 'additive' --delta-size 1.0 \
                --est-name 'diff-in-means' \
                --misspec-type 'add' --p-add 0.05 0.1 0.5

            python3 -m plotting.make_plot_inputs_misspec --data-dir 'data' --net-mdl-saved $net_mdl \
                --n $n --tau $tau --n-iters $n_iters \
                --expo-mdl-name 'frac-nbr-expo' --q $q \
                --rand-mdl-name 'restricted-genetic' --n-z 10000 --n-cutoff 1000 \
                --fitness-fn-name 'square-smd_frac-expo' --smd-weight 1.0 --expo-weight 1.0 \
                --outcome-mdl-name 'additive' --delta-size 1.0 \
                --est-name 'diff-in-means' \
                --misspec-type 'add' --p-add 0.05 0.1 0.5
            
            python3 -m plotting.make_plots_misspec --n $n --n-iters $n_iters --net-mdl-saved $net_mdl --expo-mdl-name "frac-nbr-expo-${q}" \
                --fitness-fn-name 'square-smd-1.00_frac-exposed-1.00' --tau $tau --misspec-type 'add' --p-add 0.05 0.1 0.5
        done

        ################## REMOVE MISSPECIFICATION ####################
        python3 -m plotting.make_plot_inputs_misspec --data-dir 'data' --net-mdl-saved $net_mdl \
            --n $n --tau $tau --n-iters $n_iters \
            --expo-mdl-name 'one-nbr-expo' \
            --rand-mdl-name 'graph' --n-z 10000 --n-cutoff 1000 \
            --outcome-mdl-name 'additive' --delta-size 1.0 \
            --est-name 'diff-in-means' \
            --misspec-type 'remove' --p-remove 0.05 0.1 0.5

        python3 -m plotting.make_plot_inputs_misspec --data-dir 'data' --net-mdl-saved $net_mdl \
            --n $n --tau $tau --n-iters $n_iters \
            --expo-mdl-name 'one-nbr-expo' \
            --rand-mdl-name 'graph-restricted' --n-z 10000 --n-cutoff 1000 \
            --fitness-fn-name 'square-smd_frac-expo' --smd-weight 1.0 --expo-weight 1.0 \
            --outcome-mdl-name 'additive' --delta-size 1.0 \
            --est-name 'diff-in-means' \
            --misspec-type 'remove' --p-remove 0.05 0.1 0.5
        
        python3 -m plotting.make_plot_inputs_misspec --data-dir 'data' --net-mdl-saved $net_mdl \
            --n $n --tau $tau --n-iters $n_iters \
            --expo-mdl-name 'one-nbr-expo' \
            --rand-mdl-name 'graph-restricted-genetic' --n-z 10000 --n-cutoff 1000 \
            --fitness-fn-name 'square-smd_frac-expo' --smd-weight 1.0 --expo-weight 1.0 \
            --outcome-mdl-name 'additive' --delta-size 1.0 \
            --est-name 'diff-in-means' \
            --misspec-type 'remove' --p-remove 0.05 0.1 0.5

        python3 -m plotting.make_plot_inputs_misspec --data-dir 'data' --net-mdl-saved $net_mdl \
            --n $n --tau $tau --n-iters $n_iters \
            --expo-mdl-name 'one-nbr-expo' \
            --rand-mdl-name 'restricted' --n-z 100000 --n-cutoff 1000 \
            --fitness-fn-name 'square-smd_frac-expo' --smd-weight 1.0 --expo-weight 1.0 \
            --outcome-mdl-name 'additive' --delta-size 1.0 \
            --est-name 'diff-in-means' \
            --misspec-type 'remove' --p-remove 0.05 0.1 0.5

        python3 -m plotting.make_plot_inputs_misspec --data-dir 'data' --net-mdl-saved $net_mdl \
            --n $n --tau $tau --n-iters $n_iters \
            --expo-mdl-name 'one-nbr-expo' \
            --rand-mdl-name 'restricted-genetic' --n-z 10000 --n-cutoff 1000 \
            --fitness-fn-name 'square-smd_frac-expo' --smd-weight 1.0 --expo-weight 1.0 \
            --outcome-mdl-name 'additive' --delta-size 1.0 \
            --est-name 'diff-in-means' \
            --misspec-type 'remove' --p-remove 0.05 0.1 0.5

        python3 -m plotting.make_plots_misspec --n $n --n-iters $n_iters --net-mdl-saved $net_mdl --expo-mdl-name "one-nbr-expo" \
            --fitness-fn-name 'square-smd-1.00_frac-exposed-1.00' --tau $tau --misspec-type 'remove' --p-remove 0.05 0.1 0.5

        for q in 0.50
        do
            python3 -m plotting.make_plot_inputs_misspec --data-dir 'data' --net-mdl-saved $net_mdl \
                --n $n --tau $tau --n-iters $n_iters \
                --expo-mdl-name 'frac-nbr-expo' --q $q \
                --rand-mdl-name 'graph' --n-z 10000 --n-cutoff 1000 \
                --outcome-mdl-name 'additive' --delta-size 1.0 \
                --est-name 'diff-in-means' \
                --misspec-type 'remove' --p-remove 0.05 0.1 0.5

            python3 -m plotting.make_plot_inputs_misspec --data-dir 'data' --net-mdl-saved $net_mdl \
                --n $n --tau $tau --n-iters $n_iters \
                --expo-mdl-name 'frac-nbr-expo' --q $q \
                --rand-mdl-name 'graph-restricted' --n-z 10000 --n-cutoff 1000 \
                --fitness-fn-name 'square-smd_frac-expo' --smd-weight 1.0 --expo-weight 1.0 \
                --outcome-mdl-name 'additive' --delta-size 1.0 \
                --est-name 'diff-in-means' \
                --misspec-type 'remove' --p-remove 0.05 0.1 0.5

            python3 -m plotting.make_plot_inputs_misspec --data-dir 'data' --net-mdl-saved $net_mdl \
                --n $n --tau $tau --n-iters $n_iters \
                --expo-mdl-name 'frac-nbr-expo' --q $q \
                --rand-mdl-name 'graph-restricted-genetic' --n-z 10000 --n-cutoff 1000 \
                --fitness-fn-name 'square-smd_frac-expo' --smd-weight 1.0 --expo-weight 1.0 \
                --outcome-mdl-name 'additive' --delta-size 1.0 \
                --est-name 'diff-in-means' \
                --misspec-type 'remove' --p-remove 0.05 0.1 0.5

            python3 -m plotting.make_plot_inputs_misspec --data-dir 'data' --net-mdl-saved $net_mdl \
                --n $n --tau $tau --n-iters $n_iters \
                --expo-mdl-name 'frac-nbr-expo' --q $q \
                --rand-mdl-name 'restricted' --n-z 100000 --n-cutoff 1000 \
                --fitness-fn-name 'square-smd_frac-expo' --smd-weight 1.0 --expo-weight 1.0 \
                --outcome-mdl-name 'additive' --delta-size 1.0 \
                --est-name 'diff-in-means' \
                --misspec-type 'remove' --p-remove 0.05 0.1 0.5

            python3 -m plotting.make_plot_inputs_misspec --data-dir 'data' --net-mdl-saved $net_mdl \
                --n $n --tau $tau --n-iters $n_iters \
                --expo-mdl-name 'frac-nbr-expo' --q $q \
                --rand-mdl-name 'restricted-genetic' --n-z 10000 --n-cutoff 1000 \
                --fitness-fn-name 'square-smd_frac-expo' --smd-weight 1.0 --expo-weight 1.0 \
                --outcome-mdl-name 'additive' --delta-size 1.0 \
                --est-name 'diff-in-means' \
                --misspec-type 'remove' --p-remove 0.05 0.1 0.5
            
            python3 -m plotting.make_plots_misspec --n $n --n-iters $n_iters --net-mdl-saved $net_mdl --expo-mdl-name "frac-nbr-expo-${q}" \
                --fitness-fn-name 'square-smd-1.00_frac-exposed-1.00' --tau $tau --misspec-type 'remove' --p-remove 0.05 0.1 0.5
        done


        ################## ADD-REMOVE MISSPECIFICATION ####################
        python3 -m plotting.make_plot_inputs_misspec --data-dir 'data' --net-mdl-saved $net_mdl \
            --n $n --tau $tau --n-iters $n_iters \
            --expo-mdl-name 'one-nbr-expo' \
            --rand-mdl-name 'graph' --n-z 10000 --n-cutoff 1000 \
            --outcome-mdl-name 'additive' --delta-size 1.0 \
            --est-name 'diff-in-means' \
            --misspec-type 'add-remove' --p-add 0.05 0.1 0.5 --p-remove 0.05 0.1 0.5

        python3 -m plotting.make_plot_inputs_misspec --data-dir 'data' --net-mdl-saved $net_mdl \
            --n $n --tau $tau --n-iters $n_iters \
            --expo-mdl-name 'one-nbr-expo' \
            --rand-mdl-name 'graph-restricted' --n-z 10000 --n-cutoff 1000 \
            --fitness-fn-name 'square-smd_frac-expo' --smd-weight 1.0 --expo-weight 1.0 \
            --outcome-mdl-name 'additive' --delta-size 1.0 \
            --est-name 'diff-in-means' \
            --misspec-type 'add-remove' --p-add 0.05 0.1 0.5 --p-remove 0.05 0.1 0.5
        
        python3 -m plotting.make_plot_inputs_misspec --data-dir 'data' --net-mdl-saved $net_mdl \
            --n $n --tau $tau --n-iters $n_iters \
            --expo-mdl-name 'one-nbr-expo' \
            --rand-mdl-name 'graph-restricted-genetic' --n-z 10000 --n-cutoff 1000 \
            --fitness-fn-name 'square-smd_frac-expo' --smd-weight 1.0 --expo-weight 1.0 \
            --outcome-mdl-name 'additive' --delta-size 1.0 \
            --est-name 'diff-in-means' \
            --misspec-type 'add-remove' --p-add 0.05 0.1 0.5 --p-remove 0.05 0.1 0.5

        python3 -m plotting.make_plot_inputs_misspec --data-dir 'data' --net-mdl-saved $net_mdl \
            --n $n --tau $tau --n-iters $n_iters \
            --expo-mdl-name 'one-nbr-expo' \
            --rand-mdl-name 'restricted' --n-z 100000 --n-cutoff 1000 \
            --fitness-fn-name 'square-smd_frac-expo' --smd-weight 1.0 --expo-weight 1.0 \
            --outcome-mdl-name 'additive' --delta-size 1.0 \
            --est-name 'diff-in-means' \
            --misspec-type 'add-remove' --p-add 0.05 0.1 0.5 --p-remove 0.05 0.1 0.5

        python3 -m plotting.make_plot_inputs_misspec --data-dir 'data' --net-mdl-saved $net_mdl \
            --n $n --tau $tau --n-iters $n_iters \
            --expo-mdl-name 'one-nbr-expo' \
            --rand-mdl-name 'restricted-genetic' --n-z 10000 --n-cutoff 1000 \
            --fitness-fn-name 'square-smd_frac-expo' --smd-weight 1.0 --expo-weight 1.0 \
            --outcome-mdl-name 'additive' --delta-size 1.0 \
            --est-name 'diff-in-means' \
            --misspec-type 'add-remove' --p-add 0.05 0.1 0.5 --p-remove 0.05 0.1 0.5

        python3 -m plotting.make_plots_misspec --n $n --n-iters $n_iters --net-mdl-saved $net_mdl --expo-mdl-name "one-nbr-expo" \
            --fitness-fn-name 'square-smd-1.00_frac-exposed-1.00' --tau $tau --misspec-type 'add-remove' --p-add 0.05 0.1 0.5 --p-remove 0.05 0.1 0.5

        for q in 0.50
        do
            python3 -m plotting.make_plot_inputs_misspec --data-dir 'data' --net-mdl-saved $net_mdl \
                --n $n --tau $tau --n-iters $n_iters \
                --expo-mdl-name 'frac-nbr-expo' --q $q \
                --rand-mdl-name 'graph' --n-z 10000 --n-cutoff 1000 \
                --outcome-mdl-name 'additive' --delta-size 1.0 \
                --est-name 'diff-in-means' \
                --misspec-type 'add-remove' --p-add 0.05 0.1 0.5 --p-remove 0.05 0.1 0.5

            python3 -m plotting.make_plot_inputs_misspec --data-dir 'data' --net-mdl-saved $net_mdl \
                --n $n --tau $tau --n-iters $n_iters \
                --expo-mdl-name 'frac-nbr-expo' --q $q \
                --rand-mdl-name 'graph-restricted' --n-z 10000 --n-cutoff 1000 \
                --fitness-fn-name 'square-smd_frac-expo' --smd-weight 1.0 --expo-weight 1.0 \
                --outcome-mdl-name 'additive' --delta-size 1.0 \
                --est-name 'diff-in-means' \
                --misspec-type 'add-remove' --p-add 0.05 0.1 0.5 --p-remove 0.05 0.1 0.5

            python3 -m plotting.make_plot_inputs_misspec --data-dir 'data' --net-mdl-saved $net_mdl \
                --n $n --tau $tau --n-iters $n_iters \
                --expo-mdl-name 'frac-nbr-expo' --q $q \
                --rand-mdl-name 'graph-restricted-genetic' --n-z 10000 --n-cutoff 1000 \
                --fitness-fn-name 'square-smd_frac-expo' --smd-weight 1.0 --expo-weight 1.0 \
                --outcome-mdl-name 'additive' --delta-size 1.0 \
                --est-name 'diff-in-means' \
                --misspec-type 'add-remove' --p-add 0.05 0.1 0.5 --p-remove 0.05 0.1 0.5

            python3 -m plotting.make_plot_inputs_misspec --data-dir 'data' --net-mdl-saved $net_mdl \
                --n $n --tau $tau --n-iters $n_iters \
                --expo-mdl-name 'frac-nbr-expo' --q $q \
                --rand-mdl-name 'restricted' --n-z 100000 --n-cutoff 1000 \
                --fitness-fn-name 'square-smd_frac-expo' --smd-weight 1.0 --expo-weight 1.0 \
                --outcome-mdl-name 'additive' --delta-size 1.0 \
                --est-name 'diff-in-means' \
                --misspec-type 'add-remove' --p-add 0.05 0.1 0.5 --p-remove 0.05 0.1 0.5

            python3 -m plotting.make_plot_inputs_misspec --data-dir 'data' --net-mdl-saved $net_mdl \
                --n $n --tau $tau --n-iters $n_iters \
                --expo-mdl-name 'frac-nbr-expo' --q $q \
                --rand-mdl-name 'restricted-genetic' --n-z 10000 --n-cutoff 1000 \
                --fitness-fn-name 'square-smd_frac-expo' --smd-weight 1.0 --expo-weight 1.0 \
                --outcome-mdl-name 'additive' --delta-size 1.0 \
                --est-name 'diff-in-means' \
                --misspec-type 'add-remove' --p-add 0.05 0.1 0.5 --p-remove 0.05 0.1 0.5
            
            python3 -m plotting.make_plots_misspec --n $n --n-iters $n_iters --net-mdl-saved $net_mdl --expo-mdl-name "frac-nbr-expo-${q}" \
                --fitness-fn-name 'square-smd-1.00_frac-exposed-1.00' --tau $tau --misspec-type 'add-remove' --p-add 0.05 0.1 0.5 --p-remove 0.05 0.1 0.5
        done
    done
done