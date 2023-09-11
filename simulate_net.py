import numpy as np
from pathlib import Path
import pickle
from argparse import ArgumentParser
import networkx as nx

from src.outcome_models import *
from src.network_models import *
from utils.load_from_args import get_net


def make_net(args):
    net_mdl = get_net(args)
    net_subdir = Path(args.data_dir) / 'networks' / f'{net_mdl.name}'
    net_fname = f'n-{args.n}.pkl'

    if (net_subdir / net_fname).exists():
        print(f'{net_subdir / net_fname} already exists! Skipping...')
        return
    else:
        print(f'Generating {net_subdir / net_fname}...')
        G, A = net_mdl(args.n)
        dists = dict(nx.all_pairs_bellman_ford_path_length(G))

        if not net_subdir.exists():
            net_subdir.mkdir(parents=True)
        with open(net_subdir / net_fname, 'wb') as output:
            pickle.dump((G, A, dists), output)

if __name__ == "__main__":
    parser = ArgumentParser()

    parser.add_argument('--data-dir', type=str, default='data')
    parser.add_argument('--n', type=int, default=500)
    parser.add_argument('--net-mdl-name', type=str, default='ws')
    parser.add_argument('--p', type=float, default=0.1)
    parser.add_argument('--k', type=int, default=10)
    parser.add_argument('--m', type=int, default=5)
    parser.add_argument('--n-blocks', type=int, default=5)
    parser.add_argument('--wip', type=float, default=0.05)
    parser.add_argument('--bwp', type=float, default=0.01)
    parser.add_argument('--seed', type=int, default=42)

    args = parser.parse_args()

    make_net(args)
