import numpy as np

def generate_uniform(a, b, n=1000):
    return np.random.uniform(float(a), float(b), int(n))

def generate_exponential(lmbd, n=1000):
    u = np.random.rand(int(n))
    return -np.log(1 - u) / float(lmbd)

def generate_normal_boxmuller(mu, sigma, n=1000):
    u1 = np.random.rand(int(n//2)); u2 = np.random.rand(int(n//2))
    z0 = np.sqrt(-2 * np.log(u1)) * np.cos(2 * np.pi * u2)
    z1 = np.sqrt(-2 * np.log(u1)) * np.sin(2 * np.pi * u2)
    z = np.concatenate([z0, z1]); z = z[:int(n)]
    return float(mu) + float(sigma) * z

def generate_poisson(lmbd, n=1000):
    return np.random.poisson(float(lmbd), int(n))
