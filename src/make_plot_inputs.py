
from argparse import ArgumentParser

from src.outcome_models import *
from src.exposure_models import *
from src.network_models import *
from src.fitness_fns import *
from src.estimators import *
from src.genetic_algorithms import *

from utils.load_from_args import *

def config():
    parser = ArgumentParser()

    data_args = parser.add_argument_group('data')
    data_args.add_argument('--data-dir', type=str, default='data')
    data_args.add_argument('--net-mdl-saved', type=str, default='ws_k-10_p-0.10')
    data_args.add_argument('--tau', type=float, default=0.4)
    data_args.add_argument('--n', type=int, default=500)
    data_args.add_argument('--n-iters', type=int, default=100)
    data_args.add_argument('--plt-iter', type=int, default=0)
    data_args.add_argument('--seed', default=42)
    data_args.add_argument('--out-dir', type=str, default='plotting')
    
    expo_args = parser.add_argument_group('expo_mdl')
    expo_args.add_argument('--expo-mdl-name', type=str, default='frac-nbr-expo')
    expo_args.add_argument('--q', type=float, default=0.5)

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

    outcome_args = parser.add_argument_group('outcome_mdl')
    outcome_args.add_argument('--outcome-mdl-name', type=str, default='additive')
    outcome_args.add_argument('--delta-size', type=float, default=0.5)

    estimator_args = parser.add_argument_group('estimator')
    estimator_args.add_argument('--est-name', type=str, default='diff-in-means')

    plt_args = parser.add_argument_group('plot')
    plt_args.add_argument('--xaxis_fn_name', type=str, default='smd')
    plt_args.add_argument('--yaxis_fn_name', type=str, default='frac-expo')

    args = parser.parse_args()

    return args

def get_axis_fns(args, expo_mdl):
    xaxis_fn = get_fitness_fn(args, args.xaxis_fn_name, expo_mdl)
    yaxis_fn = get_fitness_fn(args, args.yaxis_fn_name, expo_mdl)

    return xaxis_fn, yaxis_fn

def make_plotting_input(args):
    y_all, A, dists = get_data(args)
    expo_mdl = get_expo_model(args, args.expo_mdl_name)
    rand_mdl = get_rand_model(args, args.rand_mdl_name, A, dists, expo_mdl)
    outcome_mdl = get_outcome_model(args, args.outcome_mdl_name, expo_mdl, A)
    estimator = get_estimator(args, args.est_name)

    xaxis_fn, yaxis_fn = get_axis_fns(args, expo_mdl)

    out_subdir = Path(args.out_dir) / 'plotting_input' / f'{args.net_mdl_saved}' / f'n-{args.n}_it-{args.n_iters}_tau-{args.tau}'
    out_fname = f'rand-{args.rand_mdl_name}_expo-{expo_mdl.name}_xaxis-{args.xaxis_fn_name}_yaxis-{args.xaxis_fn_name}.pkl'
    mdl_names = {'rand_mdl':rand_mdl.name, 'expo_mdl': expo_mdl.name}

    if (out_subdir / out_fname).exists():
        print(f'{out_subdir / out_fname} already exists! Skipping...')
        return
    else:
        y_0, y_1 = y_all[args.plt_iter]
        z_accepted, _ = rand_mdl(y_0)
        y_obs = [outcome_mdl(z, y_0, y_1) for z in z_accepted]

        scatter_xvals = xaxis_fn(z_accepted, y_0, A)
        scatter_yvals = yaxis_fn(z_accepted, y_0, A)
        density_tau_hat = [estimator(z, y).item() for (z, y) in zip(z_accepted, y_obs)]

        if not out_subdir.exists():
            out_subdir.mkdir(parents=True)
        print(f'Saving to {out_subdir / out_fname}...')
        with open(out_subdir / out_fname, 'wb') as output:
            pickle.dump((scatter_xvals, scatter_yvals, density_tau_hat, mdl_names), output)
            
        # y_0_all, y_1_all = [y[0] for y in y_all], [y[1] for y in y_all]
        # z_all = np.array([rand_mdl(y_0)[0][1] for y_0 in y_0_all])
        # y_obs = np.array([outcome_mdl(z, y_0, y_1) for (z, y_0, y_1) in zip(z_all, y_0_all, y_1_all)])

        # scatter_xvals = [xaxis_fn(z, y_0, A) for (z, y_0) in zip(z_all, y_0_all)]
        # scatter_yvals = [yaxis_fn(z, y_0, A) for (z, y_0) in zip(z_all, y_0_all)]
        # density_tau_hat = [estimator(z, y).item() for (z, y) in zip(z_all, y_obs)]

        # if not out_subdir.exists():
        #     out_subdir.mkdir(parents=True)
        # print(f'Saving to {out_subdir / out_fname}...')
        # with open(out_subdir / out_fname, 'wb') as output:
        #     pickle.dump((scatter_xvals, scatter_yvals, density_tau_hat, mdl_names), output)




if __name__ == "__main__":
    args = config()
    make_plotting_input(args)

    
  