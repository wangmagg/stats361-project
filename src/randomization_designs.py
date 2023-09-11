import numpy as np
from src.genetic_algorithms import *

class CompleteRandomization():
    def __init__(self, n, n_z, n_cutoff, seed=42):
        self.name = 'complete'
        self.n = n
        self.n_z = n_z
        self.n_cutoff = n_cutoff
        self.rng = np.random.default_rng(seed)
    
    def sample_z(self):
        z = np.zeros(self.n)
        n_trt = self.n // 2
        z[:n_trt] = 1
        self.rng.shuffle(z)

        return z
    
    def sample_mult_z(self):
        return np.vstack([self.sample_z() for _ in range(self.n_z)])
    
    def sample_accepted_idxs(self):
        return self.rng.choice(np.arange(self.n_z), size=self.n_cutoff, replace=False)

    def sample_chosen_idx(self):
        return self.rng.integers(self.n_cutoff)
    
    def __call__(self, _):
        z_pool = self.sample_mult_z()
        accepted_idxs = self.sample_accepted_idxs()
        z_accepted = z_pool[accepted_idxs, :]
        chosen_idx = self.sample_chosen_idx()

        return z_accepted, chosen_idx

class RestrictedRandomization(CompleteRandomization):
    def __init__(self, n, n_z, n_cutoff, fitness_fn, A, seed=42):
        super().__init__(n, n_z, n_cutoff)
        self.name = f'restricted_{fitness_fn.name}'
        self.fitness_fn = fitness_fn
        self.A = A
        self.rng = np.random.default_rng(seed)

    def sample_accepted_idxs(self, z_pool, X):
        scores = self.fitness_fn(z_pool, X, self.A)
        return np.argsort(scores)[:self.n_cutoff]    
    
    def __call__(self, X):
        z_pool = self.sample_mult_z()
        accepted_idxs = self.sample_accepted_idxs(z_pool, X)
        z_accepted = z_pool[accepted_idxs, :]
        chosen_idx = self.sample_chosen_idx()

        return z_accepted, chosen_idx
    
class RestrictedRandomizationGenetic(CompleteRandomization):
    def __init__(self, n, n_z, n_cutoff, fitness_fn, A, 
                 tourn_size, cross_k, cross_rate, mut_rate, genetic_iters,
                 seed=42):
        super().__init__(n, n_z, n_cutoff)
        self.name = f'restricted-genetic_{fitness_fn.name}'
        self.fitness_fn = fitness_fn
        self.A = A
        self.rng = np.random.default_rng(seed)
        self.tourn_size = tourn_size
        self.cross_k = cross_k
        self.cross_rate = cross_rate
        self.mut_rate = mut_rate
        self.genetic_iters = genetic_iters

    def sample_accepted_idxs(self, z_pool, X):
        scores = self.fitness_fn(z_pool, X, self.A)
        return np.argsort(scores)[:self.n_cutoff]    
    
    def __call__(self, X):
        z_pool = self.sample_mult_z()
        z_pool, _ = run_genetic_alg(z_pool, self.fitness_fn, X, self.A, 
                                    self.tourn_size, self.cross_k, self.cross_rate, 
                                    self.mut_rate, self.genetic_iters, self.rng)
        accepted_idxs = self.sample_accepted_idxs(z_pool, X)
        z_accepted = z_pool[accepted_idxs, :]
        chosen_idx = self.sample_chosen_idx()

        return z_accepted, chosen_idx
    
class GraphRandomization(CompleteRandomization):
    def __init__(self, n, n_z, n_cutoff, dists, A, seed=42):
        super().__init__(n, n_z, n_cutoff)
        self.n_clusters = n
        self.name = 'graph'
        self.dists = dists
        self.A = A
        self.rng = np.random.default_rng(seed)
        self.cached_B = False

    def get_two_ball(self):
        # get two-ball for each vertex in graph
        B = []
        for i in range(self.A.shape[0]):
            r1_mask = self.A[i, :]
            r1_idxs = np.flatnonzero(r1_mask) # all indices within radius 1
            r2_mask = np.sum(self.A[r1_idxs, :], axis=0) # all indices within radius 2
            r2_idxs = np.flatnonzero(r1_mask + r2_mask) # all indices within radius 1 or 2
            B.append(r2_idxs)
        return B

    def three_net(self, B):
        n = self.A.shape[0]
        visited = np.zeros(n)
        unvisited = np.flatnonzero(visited == 0)
        V = [] # store cluster centers

        while len(unvisited) > 0:
            # randomly choose an unvisited vertex
            v = self.rng.choice(unvisited)

            # mark the vertex and its two-ball as visited
            visited[v] = 1
            visited[B[v]] = 1

            # add vertex as a cluster center
            V.append(v)

            unvisited = np.flatnonzero(visited == 0)

        # assign vertices to closest clusters
        C = np.zeros(n) # vertex assignments
        for i in range(n):
            dists_to_v = [self.dists[i][v] for v in V if v in self.dists[i]]
            if not dists_to_v:
                C[i] = V[self.rng.integers(len(V))]
            else:
                C[i] = V[np.argmin(dists_to_v)]
        
        return V, C

    def sample_z(self, V, C):
        treated_clusters = self.rng.choice(V, size=len(V) // 2, replace=False)
        z = np.in1d(C, treated_clusters).astype(int)

        return z

    def sample_mult_z(self):
        if not self.cached_B:
            self.B = self.get_two_ball()
            self.cached_B = True
        V, C = self.three_net(self.B)
        z_pool = [self.sample_z(V, C) for _ in range(self.n_z)] # treatment assignments
        self.n_clusters = len(V)
        _, cnts = np.unique(C, return_counts=True)
        self.size_per_cluster = cnts

        return np.array(z_pool)

class GraphRestrictedRandomization(GraphRandomization):
    def __init__(self, n, n_z, n_cutoff, dists, A, fitness_fn, seed=42):
        super().__init__(n, n_z, n_cutoff, dists, A, seed)
        self.name = f'graph-restricted_{fitness_fn.name}'
        self.fitness_fn = fitness_fn

    def sample_accepted_idxs(self, z_pool, X):
        scores = self.fitness_fn(z_pool, X, self.A)
        return np.argsort(scores)[:self.n_cutoff]    
    
    def __call__(self, X):
        z_pool = self.sample_mult_z()
        accepted_idxs = self.sample_accepted_idxs(z_pool, X)
        z_accepted = z_pool[accepted_idxs, :]
        chosen_idx = self.sample_chosen_idx()

        return z_accepted, chosen_idx
    
class GraphRestrictedRandomizationGenetic(GraphRandomization):
    def __init__(self, n, n_z, n_cutoff, dists, A, fitness_fn, 
                 tourn_size, cross_k, cross_rate, mut_rate, genetic_iters,
                 seed=42):
        super().__init__(n, n_z, n_cutoff, dists, A, seed)
        self.name = f'graph-restricted-genetic_{fitness_fn.name}'
        self.fitness_fn = fitness_fn
        self.A = A
        self.rng = np.random.default_rng(seed)
        self.tourn_size = tourn_size
        self.cross_k = cross_k
        self.cross_rate = cross_rate
        self.mut_rate = mut_rate
        self.genetic_iters = genetic_iters

    def sample_accepted_idxs(self, z_pool, X):
        scores = self.fitness_fn(z_pool, X, self.A)
        return np.argsort(scores)[:self.n_cutoff]    
    
    def __call__(self, X):
        z_pool = self.sample_mult_z()
        z_pool, _ = run_genetic_alg(z_pool, self.fitness_fn, X, self.A, 
                                    self.tourn_size, self.cross_k, self.cross_rate, 
                                    self.mut_rate, self.genetic_iters, self.rng)
        accepted_idxs = self.sample_accepted_idxs(z_pool, X)
        z_accepted = z_pool[accepted_idxs, :]
        chosen_idx = self.sample_chosen_idx()

        return z_accepted, chosen_idx