import numpy as np

def sample_po(n, mu, sigma, gamma, tau, A, rng):
    X = rng.normal(mu, sigma, size=n)

    mu_y = np.matmul(A, X)
    y_0 = rng.normal(mu_y, gamma)
    y_1 = y_0 + tau * np.std(y_0)

    return y_0, y_1

class AdditiveInterference():
    def __init__(self, delta, expo_mdl, A):
        self.name = f'additive-{delta:.2f}'
        self.delta = delta
        self.expo_mdl = expo_mdl
        self.A = A
    def __call__(self, z, y_0, y_1):
        return z*y_1 + (1-z)*y_0 + (1-z)*self.delta*np.std(y_0)*self.expo_mdl(z, self.A)

    
