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
            expo_scores_stand = (expo_scores - np.min(smd_scores)) / (np.max(expo_scores) - np.min(expo_scores))
        else:
            expo_scores_stand = np.zeros_like(expo_scores)

        smd_expo = self.smd_weight * smd_scores_stand + self.expo_weight * expo_scores_stand

        return smd_expo
    