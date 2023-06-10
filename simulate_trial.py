import numpy as np
import pandas as pd
from pathlib import Path
import pickle
from argparse import ArgumentParser
from functools import partial

from src.outcome_models import *
from src.exposure_models import *
from src.network_models import *
from src.randomization_designs import *
from src.fitness_fns import *
from src.estimators import *
from src.genetic_algorithms import *

from utils.load_from_args import *
import multiprocessing as mp

def print_log(net_mdl_saved, n, tau, expo_mdl_name, rand_mdl_name, outcome_mdl_name, estimator_name):
    print(f'net = {net_mdl_saved}')
    print(f'n = {n}')
    print(f'tau = {tau}')
    print(f'expo_mdl = {expo_mdl_name}')
    print(f'rand_mdl = {rand_mdl_name}')
    print(f'outcome_mdl = {outcome_mdl_name}')
    print(f'estimator = {estimator_name}')

def config():
    parser = ArgumentParser()
    parser.add_argument('--mp', action='store_true')

    data_args = parser.add_argument_group('data')
    data_args.add_argument('--data-dir', type=str, default='data')
    data_args.add_argument('--net-mdl-saved', type=str, default='ws_k-10_p-0.10')
    data_args.add_argument('--n', type=int, default=500)
    data_args.add_argument('--n-iters', type=int, default=100)
    data_args.add_argument('--tau', type=float, default=0.6)
    data_args.add_argument('--seed', default=42)
    data_args.add_argument('--out-dir', type=str, default='output')
    
    expo_args = parser.add_argument_group('expo_mdl')
    expo_args.add_argument('--expo-mdl-name', type=str, default='frac-nbr-expo-0.5')
    expo_args.add_argument('--q', type=float, default=0.5)
    
    outcome_args = parser.add_argument_group('outcome_mdl')
    outcome_args.add_argument('--outcome-mdl-name', type=str, default='additive')
    outcome_args.add_argument('--delta', type=float, default=0.8)

    rand_args = parser.add_argument_group('rand_mdl')
    rand_args.add_argument('--rand-mdl-name', type=str, default='complete')
    rand_args.add_argument('--n-z', type=int, default=int(1e5))
    rand_args.add_argument('--n-cutoff', type=int, default=int(1e3))
    rand_args.add_argument('--fitness-fn-name', type=str, default='square-smd_frac-expo')
    rand_args.add_argument('--smd-weight', type=float, default=1)
    rand_args.add_argument('--expo-weight', type=float, default=1)

    genetic_args = parser.add_argument_group('genetic')
    genetic_args.add_argument('--tourn-size', type=int, default=2)
    genetic_args.add_argument('--cross-k', type=int, default=2)
    genetic_args.add_argument('--cross-rate', type=float, default=0.95)
    genetic_args.add_argument('--mut-rate', type=float, default=0.01)
    genetic_args.add_argument('--genetic-iters', type=int, default=3)
    
    estimator_args = parser.add_argument_group('estimator')
    estimator_args.add_argument('--est-name', type=str, default='diff-in-means')

    args = parser.parse_args()

    return args

# perform trial with single data sample
def perform_trial(y, expo_mdl, rand_mdl, outcome_mdl, estimator):
    y_0, y_1 = y

    z_accepted, chosen_idx = rand_mdl(y_0)
    y_obs = outcome_mdl(z_accepted[chosen_idx, :], y_0, y_1)
    tau_hat = estimator(z_accepted[chosen_idx, :], y_obs)
    pval = get_pval(chosen_idx, z_accepted, y_obs, estimator)

    trial_res = {'rand_mdl': rand_mdl.name,
                    'expo_mdl': expo_mdl.name,
                    'outcome_mdl': outcome_mdl.name,
                    'estimator': estimator.name,
                    'tau_hat': tau_hat,
                    'pval': pval}
    
    return trial_res

def save_trial_res(args, repeated_trial_res, out_dir, out_fname):
    # calculate bias, mse, and rejection rate 
    repeated_trial_res_df = pd.DataFrame.from_records(repeated_trial_res)
    repeated_trial_res_df['tau_diff'] = repeated_trial_res_df['tau_hat'] - args.tau
    repeated_trial_res_df = repeated_trial_res_df.groupby(['rand_mdl', 'expo_mdl', 'outcome_mdl', 'estimator']).agg(
        bias = pd.NamedAgg(column="tau_diff", aggfunc=lambda x: np.mean(x)),
        mse = pd.NamedAgg(column="tau_diff", aggfunc=lambda x: np.mean(x**2)),
        rej_rate = pd.NamedAgg(column="pval", aggfunc=lambda x: np.mean(x < 0.05)))

    # save trial results
    if not out_dir.exists():
        out_dir.mkdir(parents=True)
    with open(out_dir / out_fname, 'wb') as output:
        pickle.dump(repeated_trial_res_df, output)

if __name__ == "__main__":
    args = config()    
    y_all, A, dists = get_data(args)
    expo_mdl, rand_mdl, outcome_mdl, estimator = get_models(args, A, dists)

    out_dir= Path(args.out_dir) / args.net_mdl_saved / f'n-{args.n}_it-{args.n_iters}_tau-{args.tau}'
    out_fname = f'{rand_mdl.name}_{expo_mdl.name}_{estimator.name}.pkl'

    if (out_dir / out_fname).exists():
        print(f'{out_dir / out_fname} already exists! Skipping...')
    else:
        print_log(args.net_mdl_saved, args.n, args.tau, expo_mdl.name, rand_mdl.name, outcome_mdl.name, estimator.name)

        if args.mp:
            with mp.Pool(4) as pool:
                repeated_trial_res = pool.map(partial(perform_trial, 
                                                    expo_mdl=expo_mdl, 
                                                    rand_mdl=rand_mdl, 
                                                    outcome_mdl=outcome_mdl, 
                                                    estimator=estimator), y_all)
        else:
            repeated_trial_res = list(map(partial(perform_trial, 
                                                    expo_mdl=expo_mdl, 
                                                    rand_mdl=rand_mdl, 
                                                    outcome_mdl=outcome_mdl, 
                                                    estimator=estimator), tqdm(y_all)))

        save_trial_res(args, repeated_trial_res, out_dir, out_fname)
