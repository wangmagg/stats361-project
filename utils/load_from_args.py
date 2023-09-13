
from pathlib import Path
import pickle

from src.outcome_models import *
from src.exposure_models import *
from src.network_models import *
from src.randomization_designs import *
from src.fitness_fns import *
from src.estimators import *
from src.genetic_algorithms import *
from src.network_misspec import *

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
    net_subdir = Path(args.data_dir) / 'networks' 
    
    if args.addhealth:
        with open(net_subdir / f"{args.net_mdl_saved}.pkl", 'rb') as input:
            _, A, dists = pickle.load(input)
    else:    
        with open(net_subdir / args.net_mdl_saved / f"n-{args.n}.pkl", 'rb') as input:
            _, A, dists = pickle.load(input)

    
    y_subdir = Path(args.data_dir) / 'outcomes' / args.net_mdl_saved
    
    if args.addhealth:
        with open(y_subdir / f"it-{args.n_iters}_tau-{args.tau:.1f}.pkl", "rb") as input:
            y = pickle.load(input)
    else:
        with open(y_subdir / f"n-{args.n}_it-{args.n_iters}_tau-{args.tau:.1f}.pkl", 'rb') as input:
            y = pickle.load(input)

    return y, A, dists

def _get_fitness_fn(fitness_fn_name, args, expo_mdl):
    if fitness_fn_name == 'square-smd_frac-expo':
        fitness_fn = SmdExpo(expo_mdl, args.smd_weight, args.expo_weight)
    elif fitness_fn_name == 'smd':
        fitness_fn = Smd()
    elif fitness_fn_name == 'square-smd':
        fitness_fn = SquareSmd()
    elif fitness_fn_name == 'frac-expo':
        fitness_fn = FracExposed(expo_mdl)
    elif fitness_fn_name == 'bias-term':
        fitness_fn = BiasTerm(expo_mdl)
    elif fitness_fn_name == 'variance-term':
        fitness_fn = VarianceTerm(args.sigma, args.gamma)
    elif fitness_fn_name == 'mse':
        fitness_fn = ConditionalMSE(expo_mdl, args.sigma, args.gamma, args.bias_weight, args.var_weight)
    else:
        raise ValueError(f'Unrecognized fitness function: {args.fitness_fn_name}')
    return fitness_fn

def get_fitness_fn(args, expo_mdl):
    return _get_fitness_fn(args.fitness_fn_name, args, expo_mdl)
    

def _get_expo_model(expo_mdl_name, q):
    if expo_mdl_name  == 'frac-nbr-expo':
        if isinstance(q, list):
            expo_mdl = [FracNbrExpo(q_indiv) for q_indiv in q]
        else:
            expo_mdl = FracNbrExpo(q)
    elif expo_mdl_name == 'one-nbr-expo':
        expo_mdl = OneNbrExpo()
    else:
        raise ValueError(f'Unrecognized exposure model: {expo_mdl_name}')
    return expo_mdl

def get_expo_model(args):
    if isinstance(args.expo_mdl_name, list):
        all_expo_mdls = []
        for e in args.expo_mdl_name:
            expo_mdl = _get_expo_model(e, args.q)
            if isinstance(expo_mdl, list):
                all_expo_mdls.extend(expo_mdl)
            else:
                all_expo_mdls.append(expo_mdl)
        return all_expo_mdls
    else:
        return _get_expo_model(args.expo_mdl_name, args.q)

def _get_rand_model(rand_mdl_name, args, A, dists, expo_mdl):
    n = A.shape[0]

    if rand_mdl_name == 'complete':
        rand_mdl = CompleteRandomization(n, args.n_z, args.n_cutoff, args.seed)
    elif 'restricted' in rand_mdl_name:
        fitness_fn = get_fitness_fn(args, expo_mdl)
        if rand_mdl_name == 'restricted-genetic':
            rand_mdl = RestrictedRandomizationGenetic(n, args.n_z, args.n_cutoff, fitness_fn, A, 
                                                      args.tourn_size, args.cross_k, args.cross_rate, 
                                                      args.mut_rate, args.genetic_iters, args.seed)
        elif rand_mdl_name == 'restricted':
            rand_mdl = RestrictedRandomization(n, args.n_z, args.n_cutoff, fitness_fn, A, args.seed)
        elif rand_mdl_name == 'graph-restricted':
            rand_mdl = GraphRestrictedRandomization(n, args.n_z, args.n_cutoff, dists, A, fitness_fn, args.seed)
        elif rand_mdl_name == 'graph-restricted-genetic':
            rand_mdl = GraphRestrictedRandomizationGenetic(n, args.n_z, args.n_cutoff, dists, A, fitness_fn, 
                                                           args.tourn_size, args.cross_k, args.cross_rate, 
                                                           args.mut_rate, args.genetic_iters, args.seed)
    elif args.rand_mdl_name == 'graph':
        rand_mdl = GraphRandomization(n, args.n_z, args.n_cutoff, dists, A, args.seed)

    return rand_mdl

def get_rand_model(args, A, dists, expo_mdl):
    if isinstance(expo_mdl, list):
        if isinstance(args.rand_mdl_name, list):
            return [_get_rand_model(r, args, A, dists, e) for e in expo_mdl for r in args.rand_mdl_name]
        else:
            return [_get_rand_model(args.rand_mdl_name, args, A, dists, e) for e in expo_mdl]
    else:
        return  _get_rand_model(args.rand_mdl_name, args, A, dists, expo_mdl)

def _get_outcome_model(outcome_mdl_name, args, expo_mdl, A):
    if 'additive' in outcome_mdl_name:
        if isinstance(args.delta_size, list):
            deltas = [d * args.tau for d in args.delta_size]
            return [AdditiveInterference(delta, expo_mdl, A) for delta in deltas]
        else:
            return AdditiveInterference(args.delta_size*args.tau, expo_mdl, A)
    else:
        raise ValueError(f'Unrecognized outcome model: {args.outcome_mdl_name}')


def get_outcome_model(args, expo_mdl, A):
    if isinstance(expo_mdl, list):
        all_outcome_mdls = []
        for e in expo_mdl:
            outcome_mdl = _get_outcome_model(args.outcome_mdl_name, args, e, A)
            if isinstance(outcome_mdl, list):
                all_outcome_mdls.extend(outcome_mdl)
            else:
                all_outcome_mdls.append(outcome_mdl)
        return all_outcome_mdls
    else:
        return _get_outcome_model(args.outcome_mdl_name, args, expo_mdl, A)

def _get_estimator(est_name):
    if est_name == 'diff-in-means':
        estimator = DiffMeans()
    else:
        raise ValueError(f'Unrecognized estimator: {est_name}')

    return estimator

def get_estimator(args):
    if isinstance(args.est_name, list):
        return [_get_estimator(e) for e in args.est_name]
    else:
        return _get_estimator(args.est_name)
    
def get_models(args, A, dists):
    expo_mdl = get_expo_model(args)
    rand_mdl = get_rand_model(args, A, dists, expo_mdl)
    outcome_mdl = get_outcome_model(args, expo_mdl, A)
    estimator = get_estimator(args)

    return expo_mdl, rand_mdl, outcome_mdl, estimator

def get_misspec(args, A):
    rng = np.random.default_rng(args.seed)

    if args.misspec_type == 'add':
        if isinstance(args.p_add, list):
            A_misspec = []
            dists_misspec = []
            for p_add in args.p_add:
                A_misspec_single = add_edges(A, p_add, rng)
                A_misspec.append(A_misspec_single)
                G_misspec = nx.from_numpy_array(A_misspec_single)
                dists_misspec.append(dict(nx.all_pairs_bellman_ford_path_length(G_misspec)))
        else:
            A_misspec = add_edges(A, args.p_add, rng)
            dists_misspec = dict(nx.all_pairs_bellman_ford_path_length(G_misspec))

    elif args.misspec_type == 'remove':
        if isinstance(args.p_add, list):
            A_misspec = []
            dists_misspec = []
            for p_remove in args.p_remove:
                A_misspec_single = remove_edges(A, p_remove, rng)
                A_misspec.append(A_misspec_single)
                G_misspec = nx.from_numpy_array(A_misspec_single)
                dists_misspec.append(dict(nx.all_pairs_bellman_ford_path_length(G_misspec)))
        else:
            A_misspec = remove_edges(A, args.p_remove, rng)
            dists_misspec = dict(nx.all_pairs_bellman_ford_path_length(G_misspec))

    elif args.misspec_type == 'add-remove':
        if isinstance(args.p_add, list):
            A_misspec = []
            dists_misspec = []
            for p_add, p_remove in zip(args.p_add, args.p_remove):
                A_misspec_single = add_and_remove_edges(A, p_add, p_remove, rng)
                A_misspec.append(A_misspec_single)
                G_misspec = nx.from_numpy_array(A_misspec_single)
                dists_misspec.append(dict(nx.all_pairs_bellman_ford_path_length(G_misspec)))
        else:
            A_misspec = add_and_remove_edges(A, args.p_add, args.p_remove, rng)
            dists_misspec = dict(nx.all_pairs_bellman_ford_path_length(G_misspec))

    return A_misspec, dists_misspec

def get_misspec_name(args):
    if args.misspec_type == 'add':
        if isinstance(args.p_add, list):
            misspec_name = []
            for p_add in args.p_add:
                misspec_name.append(f'add-{p_add}')
        else:
            misspec_name = f'add-{args.p_add}'

    elif args.misspec_type == 'remove':
        if isinstance(args.p_remove, list):
            misspec_name = []
            for p_remove in args.p_remove:
                misspec_name.append(f'remove-{p_remove}')
        else:
            misspec_name = f'remove-{args.p_remove}'

    elif args.misspec_type == 'add-remove':
        if isinstance(args.p_add, list):
            misspec_name = []
            for p_add, p_remove in zip(args.p_add, args.p_remove):
                misspec_name.append(f'add-{p_add}_remove-{p_remove}')
        else:
            misspec_name = f'add-{args.p_add}_remove-{args.p_remove}'

    return misspec_name
    
