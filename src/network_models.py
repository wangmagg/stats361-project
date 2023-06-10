import numpy as np
import networkx as nx

class ErdosRenyi:
    def __init__(self, p, seed):
        self.p = p
        self.seed = seed
        self.name = f'er_p-{p:.2f}'
    def __call__(self, n):
        G = nx.erdos_renyi_graph(n=n, p=self.p, seed=self.seed)
        A = nx.to_numpy_array(G)
        return G, A

class WattsStrogatz:
    def __init__(self, k, p, seed):
        self.k = k
        self.p = p
        self.seed = seed
        self.name = f'ws_k-{k}_p-{p:.2f}'
    def __call__(self, n):
        G = nx.watts_strogatz_graph(n=n, k=self.k, p=self.p, seed=self.seed)
        A = nx.to_numpy_array(G)
        return G, A
    
class BarabasiAlbert:
    def __init__(self, m, seed):
        self.m = m
        self.seed = seed
        self.name = f'ba_m-{m}'
    def __call__(self, n):
        G = nx.barabasi_albert_graph(n=n, m=self.m, seed=self.seed)
        A = nx.to_numpy_array(G)
        return G, A

class StochasticBlock:
    def __init__(self, n_blocks, wi_p, bw_p, seed):
        self.n_blocks = n_blocks
        self.wi_p = wi_p
        self.bw_p = bw_p
        self.seed = seed
        self.name = f'sb_blocks-{n_blocks}_wip-{wi_p:.2f}_bwp-{bw_p:.2f}'
    def __call__(self, n):
        block_size = n // self.n_blocks
        rem_size = n % self.n_blocks
        sizes = np.array([block_size for _ in range(self.n_blocks)])
        sizes[self.n_blocks-1] += rem_size

        density = np.zeros((self.n_blocks, self.n_blocks))
        np.fill_diagonal(density, self.wi_p)
        density[~np.eye(self.n_blocks, dtype=bool)] = self.bw_p
        G = nx.stochastic_block_model(sizes, density, seed=self.seed)
        A = nx.to_numpy_array(G)
        return G, A

if __name__ == "__main__":
    seed = 42
    
    er = ErdosRenyi(p=0.02, seed=seed)
    er_G, er_A = er(500)
    print(f'ER Density: {nx.density(er_G):.4f}')
    
    ws = WattsStrogatz(k=10, p=0.1, seed=seed)
    ws_G, ws_A = ws(500)
    print(f'WS Density: {nx.density(ws_G):.4f}')

    ba = BarabasiAlbert(m=5, seed=seed)
    ba_G, ba_A = ba(500)
    print(f'BA Density: {nx.density(ba_G):.4f}')

    sb = StochasticBlock(n_blocks=5, wi_p=0.05, bw_p=0.01, seed=seed)
    sb_G, sb_A = sb(500)
    print(f'SB Density: {nx.density(sb_G):.4f}')