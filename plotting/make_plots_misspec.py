import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from argparse import ArgumentParser
import pandas as pd

from src.outcome_models import *
from src.exposure_models import *
from src.network_models import *
from src.fitness_fns import *
from src.estimators import *
from src.genetic_algorithms import *

from utils.load_from_args import *

def config():
    parser = ArgumentParser()

    parser.add_argument('--input-dir', type=str, default='plotting')
    parser.add_argument('--out-dir', type=str, default='figs_misspec')
    parser.add_argument('--net-mdl-saved', type=str, default='ws_k-10_p-0.10')
    parser.add_argument('--tau', type=float, default=0.4)
    parser.add_argument('--n', type=int, default=500)
    parser.add_argument('--n-iters', type=int, default=1)

    parser.add_argument('--expo-mdl-name', type=str, default='frac-nbr-expo-0.50')
    parser.add_argument('--rand-mdl-name', type=str, nargs='+',
                           default=['restricted', 'restricted-genetic', 'graph', 'graph-restricted', 'graph-restricted-genetic'])
    parser.add_argument('--fitness-fn-name', type=str, default='square-smd_frac-expo')
 
    parser.add_argument('--xaxis_fn_name', type=str, default='smd')
    parser.add_argument('--yaxis_fn_name', type=str, default='frac-expo')
    parser.add_argument('--xaxis_title', type=str, default='Standardized Mean Difference')
    parser.add_argument('--yaxis_title', type=str, default='Fraction of Control Units Exposed')

    parser.add_argument('--misspec-type', type=str, default='add', choices=['add', 'remove', 'add-remove'])
    parser.add_argument('--p-remove', type=float, nargs='+', default=[0.05, 0.1, 0.5])
    parser.add_argument('--p-add', type=float, nargs='+', default=[0.05, 0.1, 0.5])

    args = parser.parse_args()

    return args

def get_scatter_title(net_mdl_saved):
    prefix = 'Accepted Allocations'
    if 'ws' in net_mdl_saved:
        return f'{prefix}: Watts-Strogatz'
    if 'sb' in net_mdl_saved:
        return f'{prefix}: Stochastic Block'
    if 'ba' in net_mdl_saved:
        return f'{prefix}: Barabasi-Albert'
    if 'er' in net_mdl_saved:
        return f'{prefix}: Erdos-Renyi'
    
def scatterplt_alloc_misspec(args):
    n_rand_mdls = len(args.rand_mdl_name)

    misspec_name = get_misspec_name(args)
    fig, ax = plt.subplots(len(misspec_name), n_rand_mdls, figsize=(20, 8), sharex=True, sharey=True)

    for i, m_name in enumerate(misspec_name):
        for j, rand_mdl_name in enumerate(args.rand_mdl_name):
            if 'restricted' in rand_mdl_name:
                rand_mdl_name_full = f'{rand_mdl_name}_{args.fitness_fn_name}'
            else:
                rand_mdl_name_full = rand_mdl_name
            in_subdir = Path(args.input_dir) / 'plotting_input' / args.net_mdl_saved / f'n-{args.n}_it-{args.n_iters}_tau-{args.tau}'
            in_fname = f'rand-{rand_mdl_name_full}_expo-{args.expo_mdl_name}_xaxis-{args.xaxis_fn_name}_yaxis-{args.yaxis_fn_name}.pkl'

            in_subdir_misspec = Path(args.input_dir) / 'plotting_input_misspec' / m_name / f'{args.net_mdl_saved}' / f'n-{args.n}_it-{args.n_iters}_tau-{args.tau}'
            in_fname_misspec = f'rand-{rand_mdl_name_full}_expo-{args.expo_mdl_name}_xaxis-{args.xaxis_fn_name}_yaxis-{args.yaxis_fn_name}.pkl'
            
            if not (in_subdir / in_fname).exists():
                print(f'{in_subdir / in_fname} does not exist')
                continue
            if not (in_subdir_misspec / in_fname_misspec).exists():
                print(f'{in_subdir_misspec / in_fname_misspec} does not exist')
                continue

            with open(in_subdir / in_fname, 'rb') as input:
                xvals, yvals, _, _, _ = pickle.load(input)
            
            with open(in_subdir_misspec / in_fname_misspec, 'rb') as input_misspec:
                xvals_misspec, yvals_misspec, _, _, _ = pickle.load(input_misspec)
            
            ax[i][j].scatter(xvals, yvals, label='oracle', s=2, alpha=0.5)
            ax[i][j].scatter(xvals_misspec, yvals_misspec, label=f'misspecified', s=2, alpha=0.5)
            ax[i][j].set_title(f'{rand_mdl_name}\n{m_name}', fontsize=12)

        #ax[i].legend()

    fig.suptitle(get_scatter_title(args.net_mdl_saved), fontsize=18)
    fig.supxlabel(args.xaxis_title, fontsize=16)
    fig.supylabel(args.yaxis_title, fontsize=16)
    handles, labels = ax[0][1].get_legend_handles_labels()
    fig.legend(handles, labels, loc='lower center', bbox_to_anchor=(0.5, -0.1))

    out_dir= Path(args.out_dir) / args.misspec_type / args.net_mdl_saved / f'n-{args.n}_it-{args.n_iters}_tau-{args.tau}'
    out_fname = f'{args.net_mdl_saved}_{args.expo_mdl_name}_{args.fitness_fn_name}.png'
    if not out_dir.exists():
        out_dir.mkdir(parents=True)

    fig.subplots_adjust(hspace=0.25, wspace=0.25)
    fig.savefig(out_dir / out_fname, bbox_inches = 'tight', dpi=600)


if __name__ == "__main__":
    args = config()
    scatterplt_alloc_misspec(args)

    