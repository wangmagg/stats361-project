import numpy as np
from tqdm import tqdm

class Smd:
    def __init__(self):
        self.name = 'smd'
        return
    
    def __call__(self, z_pool, X, A):
        # standardize X
        if X.ndim == 2:
            X_norm = (X - np.mean(X, axis=0)) / np.std(X, axis=0)
        else:
            X_norm = (X - np.mean(X)) / np.std(X)

        # calculate group means and return difference
        if z_pool.ndim == 2:
            mean_1 = np.matmul(z_pool, X_norm) / np.sum(z_pool, axis=1)
            mean_0 = np.matmul(1 - z_pool, X_norm) / np.sum(1 - z_pool, axis=1)
        else:
            mean_1 = np.matmul(z_pool, X_norm) / np.sum(z_pool)
            mean_0 = np.matmul(1 - z_pool, X_norm) / np.sum(1 - z_pool)

        return mean_1 - mean_0
    
class SquareSmd:
    def __init__(self):
        self.name = 'square-smd'
        return
    
    def __call__(self, z_pool, X, A):
        # standardize X
        if X.ndim == 2:
            X_norm = (X - np.mean(X, axis=0)) / np.std(X, axis=0)
        else:
            X_norm = (X - np.mean(X)) / np.std(X)
            
        # calculate group means and return difference
        if z_pool.ndim == 2:
            mean_1 = np.matmul(z_pool, X_norm) / np.sum(z_pool, axis=1)
            mean_0 = np.matmul(1 - z_pool, X_norm) / np.sum(1 - z_pool, axis=1)
        else:
            mean_1 = np.matmul(z_pool, X_norm) / np.sum(z_pool)
            mean_0 = np.matmul(1 - z_pool, X_norm) / np.sum(1 - z_pool)

        return np.square(mean_1 - mean_0)

class FracExposed:
    def __init__(self, expo_mdl):
        self.name = 'frac-exposed'
        self.expo_mdl = expo_mdl
    
    def __call__(self, z_pool, X, A):
        is_exposed = self.expo_mdl(z_pool, A)
        if z_pool.ndim == 2:
            return np.sum(is_exposed * (1 - z_pool), axis=1) / np.sum(1 - z_pool, axis=1)
        else:
            return np.sum(is_exposed * (1 - z_pool)) / np.sum(1 - z_pool)
            
class SmdExpo:
    def __init__(self, expo_mdl, smd_weight, expo_weight):
        self.name = f'square-smd-{smd_weight:.2f}_frac-exposed-{expo_weight:.2f}'
        self.expo_mdl = expo_mdl
        self.smd_weight = smd_weight
        self.expo_weight = expo_weight

    def __call__(self, z_pool, X, A):
        smd = SquareSmd()
        expo = FracExposed(self.expo_mdl)

        smd_scores = smd(z_pool, X, A)
        expo_scores = expo(z_pool, X, A)

        if (np.max(smd_scores) - np.min(smd_scores)) > 0:
            smd_scores_stand = (smd_scores - np.min(smd_scores)) / (np.max(smd_scores) - np.min(smd_scores))
        else:
            smd_scores_stand = np.zeros_like(smd_scores)
        if (np.max(expo_scores) - np.min(expo_scores)) > 0:
            expo_scores_stand = (expo_scores - np.min(expo_scores)) / (np.max(expo_scores) - np.min(expo_scores))
        else:
            expo_scores_stand = np.zeros_like(expo_scores)

        smd_expo = self.smd_weight * smd_scores_stand + self.expo_weight * expo_scores_stand

        return smd_expo

class BiasTerm:
    def __init__(self, expo_mdl):
        self.name = 'bias-term'
        self.expo_mdl = expo_mdl
    
    def __call__(self, z_pool, X, A):
        expo = FracExposed(self.expo_mdl)
        
        degs = np.sum(A, axis=0)
        avg_deg_1 = np.mean(degs * z_pool, axis=1)
        avg_deg_0 = np.mean(degs * (1-z_pool), axis=1)
        expo_scores = expo(z_pool, X, A)

        avg_deg_1_range = np.max(avg_deg_1) - np.min(avg_deg_1)
        avg_deg_0_range = np.max(avg_deg_0) - np.min(avg_deg_0)
        expo_scores_range = np.max(expo_scores) - np.min(expo_scores)

        if avg_deg_1_range > 0:
            avg_deg_1_stand = (avg_deg_1 - np.min(avg_deg_1)) / avg_deg_1_range
        else:
            avg_deg_1_stand = np.zeros_like(avg_deg_1)

        if avg_deg_0_range > 0:
            avg_deg_0_stand = (avg_deg_0 - np.min(avg_deg_0)) / avg_deg_0_range
        else:
            avg_deg_0_stand = np.zeros_like(avg_deg_0)

        if expo_scores_range > 0:
            expo_scores_stand = (expo_scores - np.min(expo_scores)) / (np.max(expo_scores) - np.min(expo_scores))
        else:
            expo_scores_stand = np.zeros_like(expo_scores)

        return np.absolute(avg_deg_1_stand - avg_deg_0_stand) + expo_scores_stand

class VarianceTerm:
    def __init__(self, sigma, gamma):
        self.name = f'variance-term_sigma-{sigma}_gamma-{gamma}'
        self.sigma = sigma
        self.gamma = gamma

    def __call__(self, z_pool, X, A):
        Asq = np.matmul(A, A)
        Asq_upper_mask = np.zeros_like(A, dtype=bool)
        Asq_upper_mask[np.triu_indices(Asq.shape[0])] = 1

        scores = np.zeros(z_pool.shape[0])
        #for i, z in tqdm(enumerate(z_pool), total=z_pool.shape[0]):
        for i, z in enumerate(z_pool):
            n_1 = np.sum(z)
            n_0 = np.sum(1-z)

            z_11_mask = np.matmul(np.expand_dims(z, 1), np.expand_dims(z, 0)).astype(bool)
            z_00_mask = np.matmul(np.expand_dims(1-z, 1), np.expand_dims(1-z, 0)).astype(bool)
            z_01_mask = np.matmul(np.expand_dims(z, 1), np.expand_dims(1-z, 0)).astype(bool)
        
            sum_11 = np.sum(Asq[z_11_mask & Asq_upper_mask])
            sum_00 = np.sum(Asq[z_00_mask & Asq_upper_mask])
            sum_01 = np.sum(Asq[z_01_mask & Asq_upper_mask])

            term_11 = self.sigma**2 / n_1**2 * sum_11
            term_00 = self.sigma**2 / n_1**2 * sum_00
            term_01 = 2*self.sigma**2 / (n_1 * n_0) * sum_01

            scores[i] = self.gamma**2 * (1/n_1 + 1/n_0) + term_11 + term_00 + term_01

        return scores

class ConditionalMSE:
    def __init__(self, expo_mdl, sigma, gamma, bias_weight, var_weight):
        self.name = f'mse_sigma-{sigma}_gamma-{gamma}_bias-{bias_weight:.2f}_var-{var_weight:.2f}'
        self.expo_mdl = expo_mdl
        self.sigma = sigma
        self.gamma = gamma
        self.bias_weight = bias_weight
        self.var_weight = var_weight

    def __call__(self, z_pool, X, A):
        bias_mdl = BiasTerm(self.expo_mdl)
        var_mdl = VarianceTerm(self.gamma, self.sigma)

        bias = bias_mdl(z_pool, X, A)
        var = var_mdl(z_pool, X, A)

        if np.max(bias) > np.min(bias):
            bias_stand = (bias - np.min(bias)) / (np.max(bias) - np.min(bias))
        else:
            bias_stand = np.zeros_like(bias)
        if np.max(var) > np.min(var):
            var_stand = (var - np.min(var)) / (np.max(var) - np.min(var))
        else:
            var_stand = np.zeros_like(var)

        return self.bias_weight * bias_stand + self.var_weight * var_stand
    


