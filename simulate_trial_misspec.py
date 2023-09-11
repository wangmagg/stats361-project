import numpy as np
import pandas as pd
from pathlib import Path
import pickle
from argparse import ArgumentParser

from src.outcome_models import *
from src.exposure_models import *
from src.network_models import *
from src.randomization_designs import *
from src.fitness_fns import *
from src.estimators import *
from src.genetic_algorithms import *
from src.network_misspec import *

from utils.load_from_args import *

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

    data_args = parser.add_argument_group('data')
    data_args.add_argument('--data-dir', type=str, default='data')
    data_args.add_argument('--net-mdl-saved', type=str, default='ws_k-10_p-0.10')
    data_args.add_argument('--n', type=int, default=500)
    data_args.add_argument('--n-iters', type=int, default=100)
    data_args.add_argument('--tau', type=float, default=0.4)
    data_args.add_argument('--seed', default=42)
    data_args.add_argument('--out-dir', type=str, default='output_misspec')
    
    expo_args = parser.add_argument_group('expo_mdl')
    expo_args.add_argument('--expo-mdl-name', type=str, default='frac-nbr-expo')
    expo_args.add_argument('--q', type=float, nargs='+', default=0.5)
    
    outcome_args = parser.add_argument_group('outcome_mdl')
    outcome_args.add_argument('--outcome-mdl-name', type=str, default='additive')
    outcome_args.add_argument('--delta-size', type=float, nargs='+', default=0.5)

    rand_args = parser.add_argument_group('rand_mdl')
    rand_args.add_argument('--rand-mdl-name', type=str, default='complete')
    rand_args.add_argument('--n-z', type=int, default=int(1e5))
    rand_args.add_argument('--n-cutoff', type=int, default=int(1e3))
    rand_args.add_argument('--fitness-fn-name', type=str, default='square-smd_frac-expo')
    rand_args.add_argument('--smd-weight', type=float, default=1)
    rand_args.add_argument('--expo-weight', type=float, default=1)
    rand_args.add_argument('--sigma', type=float, default=2)
    rand_args.add_argument('--gamma', type=float, default=1)

    genetic_args = parser.add_argument_group('genetic')
    genetic_args.add_argument('--tourn-size', type=int, default=2)
    genetic_args.add_argument('--cross-k', type=int, default=2)
    genetic_args.add_argument('--cross-rate', type=float, default=0.95)
    genetic_args.add_argument('--mut-rate', type=float, default=0.01)
    genetic_args.add_argument('--genetic-iters', type=int, default=3)
    
    estimator_args = parser.add_argument_group('estimator')
    estimator_args.add_argument('--est-name', type=str, default='diff-in-means')

    misspec_args = parser.add_argument_group('misspec')
    misspec_args.add_argument('--misspec-type', type=str, default='add', choices=['add', 'remove', 'add-remove'])
    misspec_args.add_argument('--p-remove', type=float, default=0.05)
    misspec_args.add_argument('--p-add', type=float, default=0.05)

    args = parser.parse_args()

    return args

# perform trial with single data sample
def perform_trial(data, expo_mdl, rand_mdl, outcome_mdl, estimator, tau):
    y, assignment = data
    y_0, y_1 = y
    z_accepted, chosen_idx = assignment 

    y_obs = outcome_mdl(z_accepted[chosen_idx, :], y_0, y_1)
    tau_hat = estimator(z_accepted[chosen_idx, :], y_obs)
    pval = get_pval(chosen_idx, z_accepted, y_obs, estimator)

    trial_res = {'rand_mdl': rand_mdl.name,
                 'expo_mdl': expo_mdl.name,
                 'outcome_mdl': outcome_mdl.name,
                 'estimator': estimator.name,
                 'tau_hat': tau_hat,
                 'tau': tau*np.std(y_0),
                 'pval': pval}
    
    return trial_res

def save_trial_res(args, repeated_trial_res, out_dir, out_fname):

    # calculate bias, mse, and rejection rate 
    repeated_trial_res_df = pd.DataFrame.from_records(repeated_trial_res)
    repeated_trial_res_df['tau_diff'] = repeated_trial_res_df['tau_hat'] - repeated_trial_res_df['tau']
    repeated_trial_res_df = repeated_trial_res_df.groupby(['rand_mdl', 'expo_mdl', 'outcome_mdl', 'estimator']).agg(
        bias = pd.NamedAgg(column="tau_diff", aggfunc=lambda x: np.mean(x)),
        mse = pd.NamedAgg(column="tau_diff", aggfunc=lambda x: np.mean(x**2)),
        rej_rate = pd.NamedAgg(column="pval", aggfunc=lambda x: np.mean(x < 0.05)))

    print(repeated_trial_res_df)

    # save trial results
    if not out_dir.exists():
        out_dir.mkdir(parents=True)

    res_dict = {'params': vars(args),
                'res': repeated_trial_res_df}
    
    with open(out_dir / out_fname, 'wb') as output:
        pickle.dump(res_dict, output)

if __name__ == "__main__":
    args = config()    
    y_all, A, dists = get_data(args)
    A_misspec, dists_misspec = get_misspec(args, A)
    misspec_name = get_misspec_name(args)
    
    expo_mdl = get_expo_model(args)
    rand_mdl = get_rand_model(args, A_misspec, dists_misspec, expo_mdl)
    outcome_mdl = get_outcome_model(args, expo_mdl, A)
    estimator = get_estimator(args)

    out_dir = Path(args.out_dir) / misspec_name / args.net_mdl_saved / f'n-{args.n}_it-{args.n_iters}_tau-{args.tau}'
    out_fname = f'{args.rand_mdl_name}.pkl'

    if (out_dir / out_fname).exists():
        print(f'{out_dir / out_fname} already exists! Skipping...')
    else:
        print(f'Running simulations for: {out_dir / out_fname}')
        all_trial_res = []
        for (y_0, y_1) in tqdm(y_all):
                assignment = rand_mdl(y_0)
                trial_res = perform_trial(((y_0, y_1), assignment), expo_mdl, rand_mdl, outcome_mdl, estimator, args.tau)
                all_trial_res.append(trial_res)

        save_trial_res(args, all_trial_res, out_dir, out_fname)
