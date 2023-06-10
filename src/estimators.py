import numpy as np

class DiffMeans:
    def __init__(self):
        self.name = 'diff-in-means'
    
    def __call__(self, z, y_obs):
        if y_obs.ndim > 1:
             mean_1 = np.diag(np.matmul(z, np.transpose(y_obs))) / np.sum(np.atleast_2d(z), axis=1)
             mean_0 = np.diag(np.matmul(1 - z, np.transpose(y_obs))) / np.sum(np.atleast_2d(1-z), axis=1)
        else:
            mean_1 = np.matmul(z, y_obs) / np.sum(np.atleast_2d(z), axis=1)
            mean_0 = np.matmul(1 - z, y_obs) / np.sum(np.atleast_2d(1-z), axis=1)
        return np.squeeze(mean_1 - mean_0)
    
def get_pval(chosen_idx, z_accepted, y_obs, estimator):
    t_obs = estimator(z_accepted[chosen_idx, :], y_obs)
    t_null = estimator(z_accepted, y_obs)
    return np.mean(abs(t_null) >= abs(t_obs))