import numpy as np

def add_edges(A, p, rng):
    A_mod = np.copy(A)

    upper_tri_mask = np.zeros_like(A, dtype=int)
    upper_tri = np.triu_indices(A.shape[0])
    upper_tri_mask[upper_tri] = 1 

    edge_tuples_to_add = np.nonzero((1 - A_mod).astype(int) & upper_tri_mask)
    n_edges = np.sum(A_mod) // 2
    n_add = int(min(n_edges, len(edge_tuples_to_add[0])) * p)

    which_add = rng.integers(len(edge_tuples_to_add[0]), size=n_add)
    for i in which_add:
        A_mod[edge_tuples_to_add[0][i], edge_tuples_to_add[1][i]] = 1

    return A_mod

def remove_edges(A, p, rng):
    A_mod = np.copy(A)

    upper_tri_mask = np.zeros_like(A, dtype=int)
    upper_tri = np.triu_indices(A.shape[0])
    upper_tri_mask[upper_tri] = 1 

    edge_tuples_to_remove = np.nonzero(A_mod.astype(int) & upper_tri_mask)
    n_edges = np.sum(A_mod) // 2
    n_remove = int(n_edges * p)

    which_remove = rng.integers(len(edge_tuples_to_remove[0]), size=n_remove)
    for i in which_remove:
        A_mod[edge_tuples_to_remove[0][i], edge_tuples_to_remove[1][i]] = 0
    
    return A_mod

def add_and_remove_edges(A, p_add, p_remove, rng):
    A_mod = np.copy(A)

    n_edges = np.sum(A_mod) // 2

    upper_tri_mask = np.zeros_like(A, dtype=int)
    upper_tri = np.triu_indices(A.shape[0])
    upper_tri_mask[upper_tri] = 1 

    edge_tuples_to_add = np.nonzero((1 - A_mod).astype(int) & upper_tri_mask)
    edge_tuples_to_remove = np.nonzero(A_mod.astype(int) & upper_tri_mask)

    n_add = int(n_edges * p_add)
    n_remove = int(n_edges * p_remove)

    which_add = rng.integers(len(edge_tuples_to_add[0]), size=n_add)
    which_remove = rng.integers(len(edge_tuples_to_remove[0]), size=n_remove)

    for i in which_add:
        A_mod[edge_tuples_to_add[0][i], edge_tuples_to_add[1][i]] = 1
    for i in which_remove:
        A_mod[edge_tuples_to_remove[0][i], edge_tuples_to_remove[1][i]] = 0

    return A_mod