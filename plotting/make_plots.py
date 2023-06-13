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
    parser.add_argument('--out-dir', type=str, default='figs')
    parser.add_argument('--net-mdl-saved', type=str, default='ws_k-10_p-0.10')
    parser.add_argument('--tau', type=float, default=0.4)
    parser.add_argument('--n', type=int, default=500)
    parser.add_argument('--n-iters', type=int, default=100)

    parser.add_argument('--expo-mdl-name', type=str, default='frac-nbr-expo-0.50')
    parser.add_argument('--rand-mdl-name', type=str, nargs='+',
                           default=['complete', 'restricted', 'restricted-genetic', 'graph'])

    parser.add_argument('--xaxis_fn_name', type=str, default='smd')
    parser.add_argument('--yaxis_fn_name', type=str, default='frac-expo')
    parser.add_argument('--xaxis_title', type=str, default='Standardized Mean Difference')
    parser.add_argument('--yaxis_title', type=str, default='Fraction of Control Units Exposed')

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
    
def scatterplt_alloc(args):
    # plt.rcParams['text.usetex'] = True

    fig, ax = plt.subplots(1, 2, figsize=(10, 5))

    for rand_mdl_name in args.rand_mdl_name:
        in_subdir = Path(args.input_dir) / 'plotting_input' / f'{args.net_mdl_saved}' / f'n-{args.n}_it-{args.n_iters}_tau-{args.tau}'
        in_fname = f'rand-{rand_mdl_name}_expo-{args.expo_mdl_name}_xaxis-{args.xaxis_fn_name}_yaxis-{args.xaxis_fn_name}.pkl'
        
        with open(in_subdir / in_fname, 'rb') as input:
            xvals, yvals, tau_hats, mdl_names = pickle.load(input)
        
        ax[0].scatter(xvals, yvals, label=rand_mdl_name, s=2, alpha=0.5)
        sns.kdeplot(tau_hats, bw_adjust=1.5, ax=ax[1], fill=True, label=rand_mdl_name)


    ax[1].axvline(x=args.tau, linestyle='--', color='black', label=r'$\tau$', linewidth=1)

    ax[0].set_xlabel(args.xaxis_title, fontsize=14)
    ax[0].set_ylabel(args.yaxis_title, fontsize=14)
    ax[0].set_title('Interference vs Balance', fontsize=16)

    ax[1].set_xlabel(r'$\hat{\tau}$', fontsize=14)
    ax[1].set_ylabel('Density', fontsize=14)
    ax[1].set_title('Effect Estimate', fontsize=16)
    #ax[1].legend()


    fig.suptitle(get_scatter_title(args.net_mdl_saved), fontsize=18)
    handles, labels = ax[1].get_legend_handles_labels()
    fig.legend(handles, labels, loc='lower center', ncol=5, bbox_to_anchor=(0.5, -0.1))
    
    out_dir= Path(args.out_dir) / f'{args.net_mdl_saved}' / f'n-{args.n}_it-{args.n_iters}_tau-{args.tau}'
    expo_mdl_full_name = mdl_names['expo_mdl']
    out_fname = f'{args.net_mdl_saved}_{expo_mdl_full_name}.png'
    if not out_dir.exists():
        out_dir.mkdir(parents=True)

    fig.savefig(out_dir / out_fname, bbox_inches = 'tight', dpi=600)

if __name__ == "__main__":
    args = config()
    scatterplt_alloc(args)

    