import pickle
import pandas as pd
from pathlib import Path
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument('--net-mdl-saved', nargs='+', type=str, default=['ws_k-10_p-0.10', 'er_p-0.02', 'ba_m-5', 'sb_blocks-5_wip-0.05_bwp-0.01'])
parser.add_argument('--n', nargs='+', type=int, default=[100, 500])
parser.add_argument('--n-iters', nargs='+', type=int, default=[500])
parser.add_argument('--tau', nargs='+', type=float, default=[0, 0.4, 0.8])
parser.add_argument('--seed', default=42)
parser.add_argument('--out-dir', type=str, default='output')
parser.add_argument('--csv-dir', type=str, default='csvs')
args = parser.parse_args()

output_dir = Path(args.out_dir)
csv_dir = Path(args.csv_dir)

if not csv_dir.exists():
    csv_dir.mkdir()

for net_mdl_name in args.net_mdl_saved:
    for n in args.n:
        for n_iter in args.n_iters:
            for tau in args.tau:
                output_subdir =  output_dir / net_mdl_name / f'n-{n}_it-{n_iter}_tau-{tau:.1f}'

                if output_subdir.exists():
                    res_df_ls = []
                    pkl_files = list((output_subdir).glob('*.pkl'))
                    for pkl_f in pkl_files:
                        with open(pkl_f, 'rb') as input:
                            res_dict = pickle.load(input)
                            res_df = res_dict['res']
                            res_df_ls.append(res_df)
            
                    res_df = pd.concat(res_df_ls)
                    res_df = res_df.sort_values(by=["rand_mdl", "expo_mdl", "outcome_mdl", "estimator"])
                    
                    csv_subdir = csv_dir / net_mdl_name 
                    if not csv_subdir.exists():
                        csv_subdir.mkdir()
                    res_df.to_csv(csv_subdir / f'n-{n}_it-{n_iter}_tau-{tau:.1f}.csv')