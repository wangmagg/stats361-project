import numpy as np

# k point crossover for a single pair of parent allocations
def crossover(z_par1, z_par2, cross_k, rng):
    for _ in range(cross_k):
        cross_loc = rng.integers(len(z_par1))

        # get right-hand side of crossover point in both parents
        z_par1_rhs = np.copy(z_par1[cross_loc:]) 
        z_par2_rhs = np.copy(z_par2[cross_loc:]) 

        # swap right-hand sides 
        z_par1[cross_loc:] = z_par2_rhs 
        z_par2[cross_loc:] = z_par1_rhs

    return z_par1, z_par2

# introduce mutations in pool of allocations at specified rate
def mutation(z_pool, rate, rng):
    mut_loc = rng.binomial(1, rate, size=z_pool.shape)
    z_pool[mut_loc == 1] = 1 - z_pool[mut_loc == 1]

    return z_pool

# "tournament" to choose a parent to mate
def tournament(scores, tourn_size, rng):
    tourn_block_idxs = rng.choice(np.arange(len(scores)), tourn_size, replace=False)
    tourn_block_scores = scores[tourn_block_idxs]
    winner = tourn_block_idxs[np.argmin(tourn_block_scores)]

    return winner

def run_genetic_alg(z_pool, fitness_fn, X, A, tourn_size, cross_k, cross_rate, mut_rate, genetic_iters, rng):
    init_pool_size = z_pool.shape[0]

    for _ in range(genetic_iters):
        scores = fitness_fn(z_pool, X, A) + 2 * np.abs(0.5 - np.mean(z_pool, axis=1))

        # use tournament selection to make mating pool
        winners = np.array([tournament(scores, tourn_size, rng) for _ in range(len(scores))])
        z_pool_mate = z_pool[winners, :]
        rng.shuffle(z_pool_mate)

        # split mating pool into two sets of parents
        mate_split = z_pool_mate.shape[0] // 2 
        z_pool_par1 = z_pool_mate[ :mate_split, :]
        z_pool_par2 = z_pool_mate[mate_split:, :]
        
        # identify which mating pairs will have crossover
        which_cross = rng.binomial(1, cross_rate, z_pool_par1.shape[0])
        z_pool_par1_cross = z_pool_par1[which_cross == 1, :]
        z_pool_par2_cross = z_pool_par2[which_cross == 1, :]

        # if a pair is designated as a crossover pair, make children with crossover
        # otherwise, children are exact copies of parents
        z_pool_chil_cross = np.vstack([crossover(z_par1, z_par2, cross_k, rng) for 
                                       (z_par1, z_par2) in zip(z_pool_par1_cross, z_pool_par2_cross)])
        z_pool_chil_copy = np.vstack((z_pool_par1[which_cross == 0, :], z_pool_par2[which_cross == 0, :])) 
        z_pool_chil = np.vstack((z_pool_chil_copy, z_pool_chil_cross))
        
        # introduce mutations in children
        z_pool_chil_mut = mutation(z_pool_chil, mut_rate, rng)

        # combine parent and child generations
        z_pool_new = np.vstack((z_pool, z_pool_chil_mut))
        new_scores = fitness_fn(z_pool_new, X, A) + 2 * np.abs(0.5 - np.mean(z_pool_new, axis=1))
        keep = np.argsort(new_scores)[:init_pool_size]
        z_pool = z_pool_new[keep, :]

        # remove allocations that are all treatment or all control
        # all_0_mask = np.sum(z_pool, axis=1) == 0
        # all_1_mask = np.sum(z_pool, axis=1) == z_pool.shape[1]
        # z_pool = z_pool[~all_0_mask & ~all_1_mask, :]
    
    return z_pool, new_scores[keep]