import numpy as np

class OneNbrExpo:
    def __init__(self):
        self.name = 'one-nbr-expo'
    def __call__(self, z, A):
        return np.matmul(z, A) >= 1 

class FracNbrExpo:
    def __init__(self, q):
        self.q = q
        self.name = f'frac-nbr-expo-{q:.2f}'
    def __call__(self, z, A):
        return np.matmul(z, A) >= self.q * np.sum(A, axis=0)