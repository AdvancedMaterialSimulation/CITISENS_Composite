import numpy as np
from scipy.interpolate import interp1d

def uniform(trajs, N=1000):
    """
    Uniformly resamples a trajectory based on its cumulative distance.
    
    Parameters:
    trajs (np.array): Input trajectory points as a NumPy array of shape (M, D),
                      where M is the number of points and D is the dimensionality.
    N (int, optional): Number of uniformly spaced points to sample along the trajectory. Default is 1000.
    
    Returns:
    trajs (np.array): Resampled trajectory points of shape (N, D).
    """
    
    # Compute the differences between consecutive points in the trajectory
    dif = np.diff(trajs, axis=0)
    
    # Compute the Euclidean distance between consecutive points
    dist = np.linalg.norm(dif, axis=1)
    
    # Compute the cumulative distance along the trajectory
    dist = np.cumsum(dist)
    
    # Add the starting point (distance = 0) to the cumulative distances
    dist = np.concatenate(([0], dist))

    # Generate a uniform spacing of distances
    t_span = np.linspace(0, dist[-1], N)

    # Interpolate the trajectory at the uniformly spaced distances
    f = interp1d(dist, trajs, axis=0)
    trajs = f(t_span)

    return trajs
