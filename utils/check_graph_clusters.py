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
    data_args.add_argument('--seed', default=42)

    rand_args = parser.add_argument_group('rand_mdl')
    rand_args.add_argument('--rand-mdl-name', type=str, default='graph')
    rand_args.add_argument('--n-z', type=int, default=int(1e3))
    rand_args.add_argument('--n-cutoff', type=int, default=int(1e3))

    args = parser.parse_args()

    return args

if __name__ == "__main__":
    args = config()

    y_all, A, dists = get_data(args)
    rand_mdl = get_rand_model(args, A, dists, None)
    print(f'{args.net_mdl_saved}_n-{args.n}_it-{args.n_iters}_tau-{args.tau}')

    n_clusters = np.zeros(len(y_all))
    avg_cluster_sizes = np.zeros(len(y_all))
    min_cluster_sizes = np.zeros(len(y_all))
    max_cluster_sizes = np.zeros(len(y_all))
    sd_cluster_sizes = np.zeros(len(y_all))
    for i, (y_0, _) in tqdm(enumerate(y_all), total=len(y_all)):
        rand_mdl(y_0)
        n_clusters[i] = rand_mdl.n_clusters
        avg_cluster_sizes[i] = np.mean(rand_mdl.size_per_cluster)
        min_cluster_sizes[i] = np.min(rand_mdl.size_per_cluster)
        max_cluster_sizes[i] = np.max(rand_mdl.size_per_cluster)
        sd_cluster_sizes[i] = np.std(rand_mdl.size_per_cluster)

    print(np.mean(n_clusters), np.std(n_clusters))
    print(np.mean(min_cluster_sizes), np.mean(max_cluster_sizes), np.mean(avg_cluster_sizes), np.mean(sd_cluster_sizes))