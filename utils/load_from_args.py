
from pathlib import Path
import pickle

from src.outcome_models import *
from src.exposure_models import *
from src.network_models import *
from src.randomization_designs import *
from src.fitness_fns import *
from src.estimators import *
from src.genetic_algorithms import *

def get_net(args):
    if 'er' in args.net_mdl_name:
        net_mdl = ErdosRenyi(args.p, args.seed)
    elif 'ws' in args.net_mdl_name:
        net_mdl = WattsStrogatz(args.k, args.p, args.seed)
    elif 'ba' in args.net_mdl_name:
        net_mdl = BarabasiAlbert(args.m, args.seed)
    elif 'sb' in args.net_mdl_name:
        net_mdl = StochasticBlock(args.n_blocks, args.wip, args.bwp, args.seed)
    else:
        raise ValueError('Unrecognized network model')
    
    return net_mdl

def get_data(args):
    net_subdir = Path(args.data_dir) / 'networks' / args.net_mdl_saved
    with open(net_subdir / f"n-{args.n}.pkl", 'rb') as input:
        _, A, dists = pickle.load(input)

    y_subdir = Path(args.data_dir) / 'outcomes' / args.net_mdl_saved
    with open(y_subdir / f"n-{args.n}_it-{args.n_iters}_tau-{args.tau:.1f}.pkl", 'rb') as input:
        y = pickle.load(input)

    return y, A, dists

def get_fitness_fn(args, fitness_fn_name, expo_mdl):
    if fitness_fn_name == 'square-smd_frac-expo':
        fitness_fn = SmdExpo(expo_mdl, args.smd_weight, args.expo_weight)
    elif fitness_fn_name == 'smd':
        fitness_fn = Smd()
    elif fitness_fn_name == 'square-smd':
        fitness_fn = SquareSmd()
    elif fitness_fn_name == 'frac-expo':
        fitness_fn = FracExposed(expo_mdl)
    else:
        raise ValueError(f'Unrecognized fitness function: {fitness_fn_name}')
    return fitness_fn
    
def get_expo_model(args, expo_mdl_name):
    if expo_mdl_name  == 'frac-nbr-expo':
        expo_mdl = FracNbrExpo(args.q)
    elif expo_mdl_name == 'one-nbr-expo':
        expo_mdl = OneNbrExpo()
    else:
        raise ValueError(f'Unrecognized exposure model: {expo_mdl_name}')
    return expo_mdl

def get_rand_model(args, rand_mdl_name, A, dists, expo_mdl):
    n = A.shape[0]

    if rand_mdl_name == 'complete':
        rand_mdl = CompleteRandomization(n, args.n_z, args.n_cutoff, args.seed)
    elif 'restricted' in args.rand_mdl_name:
        fitness_fn = get_fitness_fn(args, args.fitness_fn_name, expo_mdl)
        if args.rand_mdl_name == 'restricted-genetic':
            rand_mdl = RestrictedRandomizationGenetic(n, args.n_z, args.n_cutoff, fitness_fn, A, 
                                                      args.tourn_size, args.cross_k, args.cross_rate, 
                                                      args.mut_rate, args.genetic_iters, args.seed)
        else:
            rand_mdl = RestrictedRandomization(n, args.n_z, args.n_cutoff, fitness_fn, A, args.seed)
    elif rand_mdl_name == 'graph':
        rand_mdl = GraphRandomization(n, args.n_z, args.n_cutoff, dists, A, args.seed)

    return rand_mdl

def get_outcome_model(args, outcome_mdl_name, expo_mdl, A):
    if 'additive' in outcome_mdl_name:
        outcome_mdl = AdditiveInterference(args.delta, expo_mdl, A)
    else:
        raise ValueError(f'Unrecognized outcome model: {outcome_mdl_name}')
    return outcome_mdl

def get_estimator(args, est_name):
    if est_name == 'diff-in-means':
        estimator = DiffMeans()
    else:
        raise ValueError(f'Unrecognized estimator: {est_name}')

    return estimator
    
def get_models(args, A, dists):
    expo_mdl = get_expo_model(args, args.expo_mdl_name)
    rand_mdl = get_rand_model(args, args.rand_mdl_name, A, dists, expo_mdl)
    outcome_mdl = get_outcome_model(args, args.outcome_mdl_name, expo_mdl, A)
    estimator = get_estimator(args, args.est_name)

    return expo_mdl, rand_mdl, outcome_mdl, estimator