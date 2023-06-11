import pickle
import pandas as pd
from pathlib import Path

output_dir = Path('output')
csv_dir = Path('csvs')

if not csv_dir.exists():
    csv_dir.mkdir()

ns = [100, 500]
taus = [0, 0.4, 0.8]
net_mdl_names = ['ws_k-10_p-0.10', 'er_p-0.02', 'ba_m-5', 'sb_blocks-5_wip-0.05_bwp-0.01']

for net_mdl_name in net_mdl_names:
    for n in ns:
        for tau in taus:
            output_subdir =  output_dir / net_mdl_name / f'n-{n}_it-500_tau-{tau:.1f}'

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
                res_df.to_csv(csv_subdir / f'n-{n}_it-500_tau-{tau:.1f}.csv')