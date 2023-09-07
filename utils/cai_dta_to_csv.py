import pandas as pd
from pathlib import Path
from argparse import ArgumentParser

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument('--data-dir', type=str, default='data/cai')
    args = parser.parse_args()

    cai_dir = Path(args.data_dir)

    for f_name in cai_dir.glob('*.dta'):
        print(f_name)
        data = pd.io.stata.read_stata(f_name)
        data.to_csv(cai_dir / f'{f_name.stem}.csv')
        # print(data)