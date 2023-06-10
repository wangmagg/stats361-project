#!/bin/bash

for n in 100 500 1000
do
    python3 -m simulate_net --n $n --net-mdl-name 'er' --p 0.02 --seed 42
    python3 -m simulate_net --n $n --net-mdl-name 'ws' --p 0.1 --k 10 --seed 42
    python3 -m simulate_net --n $n --net-mdl-name 'ba' --m 5 --seed 42
    python3 -m simulate_net --n $n --net-mdl-name 'sb' --n-blocks 5 --wip 0.05 --bwp 0.01 --seed 42
done