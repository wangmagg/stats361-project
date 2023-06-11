import numpy as np
from pathlib import Path
import pickle
from argparse import ArgumentParser

from src.outcome_models import *
from src.network_models import *

def make_data(args):
    y_subdir = Path(args.data_dir) / 'outcomes' / args.net_mdl_saved
    y_fname = f"n-{args.n}_it-{args.n_iters}_tau-{args.tau:.1f}.pkl"

    if (y_subdir / y_fname).exists():
        print(f"{y_subdir / y_fname} already exists! Skipping...")
        return
    else:
        print(f"Generating {y_subdir / y_fname}")
        
        rng = np.random.default_rng(args.seed)

        net_subdir = Path(args.data_dir) / 'networks' / args.net_mdl_saved
        with open(net_subdir / f"n-{args.n}.pkl", 'rb') as input:
            _, A, _ = pickle.load(input)

        all_y = []
        for _ in range(args.n_iters):
            y_0, y_1 = sample_po(args.n, args.mu, args.sigma, args.gamma, args.tau, A, rng)
            all_y.append((y_0, y_1))

        if not y_subdir.exists():
            y_subdir.mkdir(parents=True)
        with open(y_subdir / y_fname, "wb") as output:
            pickle.dump(all_y, output)

if __name__ == "__main__":
    parser = ArgumentParser()

    parser.add_argument('--data-dir', type=str, default='data')
    parser.add_argument('--n', type=int, default=500)
    parser.add_argument('--mu', type=float, default=1)
    parser.add_argument('--sigma', type=float, default=2)
    parser.add_argument('--gamma', type=float, default=1)
    parser.add_argument('--tau', type=float, default=0.6)
    parser.add_argument('--n-iters', type=int, default=100)
    parser.add_argument('--seed', type=int, default=42)
    parser.add_argument('--net-mdl-saved', type=str, default='ws_k-10_p-0.10')

    args = parser.parse_args()

    make_data(args)
