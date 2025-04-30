import numpy as np

# Define a lambda function to check if two points are very close to each other
eq_vec = lambda p1, p2: np.linalg.norm(np.array(p2) - np.array(p1)) < 1e-4

# Define a lambda function to check if a point r0 (in 2D) is very close to any of the points in points_ext
inside = lambda points_ext, r0: np.sum([eq_vec(r0[:2], ip) for ip in points_ext]) != 0

def is_semicylinder_mesh(itraj, Lx, Ly):
    """
    Checks if a given trajectory represents a line segment located on the boundary
    of a rectangular domain, which could be part of a semicylinder mesh generation.

    Args:
        itraj (numpy.ndarray): A 2D numpy array representing the trajectory,
                               where each row is a point [x, y, ...]. Only the
                               first two columns (x, y coordinates) are considered.
        Lx (float): The length of the rectangular domain in the x-direction.
        Ly (float): The length of the rectangular domain in the y-direction.

    Returns:
        bool: True if the trajectory is a straight line segment located on one
              of the edges of the rectangle defined by (0, 0), (Lx, 0), (Lx, Ly), and (0, Ly).
              False otherwise.
    """

    # Check if the trajectory is essentially a straight line along one of the axes.
    # np.std(itraj, axis=0) calculates the standard deviation along each column (x, y, ...).
    # If the standard deviation for two of the spatial dimensions (presumably x and y) is very small,
    # it means the points in the trajectory have very little variation in those dimensions, indicating a line.
    is_line = np.sum(np.std(itraj[:, :2], axis=0) < 1e-4) == 1 # Modified to check only the first two columns

    # Get the first point of the trajectory. We use this to check if the line lies on the boundary.
    r0 = itraj[0]

    # Define the four corner points of the rectangular domain.
    points_ext = [
        [0  , 0  ],
        [0  , Ly ],
        [Lx , Ly ],
        [Lx , 0  ]
    ]

    # Check if the starting point of the trajectory is very close to any of the corner points
    # of the rectangular boundary. This helps determine if the line segment lies on the boundary.
    in_ext = inside(points_ext, r0)

    # If the trajectory is a straight line (in 2D) AND its starting point lies on one of the corners
    # of the rectangular domain, then we consider it to be a line segment on the boundary.
    if is_line and in_ext:
        return True
    else:
        return False