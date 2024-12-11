import numpy as np
def transform(vec_x, vec_z, r0, ry, N=30):
    """
    Transforms points from a local circular region to a global 3D space using the provided
    reference vectors and origin. 

    Parameters:
    vec_x (np.array): A 3D vector defining the x-axis direction in the global space.
    vec_z (np.array): A 3D vector defining the z-axis direction in the global space.
    r0 (np.array): A 3D vector representing the origin of the transformed circle in the global space.
    ry (float): The radius of the circular region to be transformed.
    N (int, optional): Number of points in the span grid along x and y directions. Default is 30.

    Returns:
    xms, yms, zms (np.array): Arrays of transformed x, y, and z coordinates in the global space.
    """

    # Create a grid of points in the x-y plane within a bounding box [-2*ry, 2*ry]
    x_span = np.linspace(-2 * ry, 2 * ry, N)
    y_span = np.linspace(-2 * ry, 2 * ry, N)
    xms, yms = np.meshgrid(x_span, y_span)

    # Compute the distance of each point from the origin in the local plane
    R = np.sqrt(xms**2 + yms**2)

    # Filter out points outside the circular region of radius `ry`
    xms = xms[R < ry]
    yms = yms[R < ry]
    zms = np.zeros_like(xms)  # Initialize z-coordinates to zero (local plane)

    # Flatten the arrays to simplify transformation
    xms = xms.flatten()
    yms = yms.flatten()
    zms = zms.flatten()

    # Normalize the reference vectors to ensure orthogonality
    vec_x = vec_x / np.linalg.norm(vec_x)
    vec_z = vec_z / np.linalg.norm(vec_z)

    # Compute the y-axis direction using the cross product of vec_x and vec_z
    vec_y = np.cross(vec_x, vec_z)

    # Create the transformation matrix from the local plane to the global space
    mat_change = np.array([vec_x, vec_y, vec_z]).T

    # Apply the transformation to the points in the local plane
    xms, yms, zms = np.dot(mat_change, np.array([xms, yms, zms]))

    # Translate the points to the global origin `r0`
    xms = xms + r0[0]
    yms = yms + r0[1]
    zms = zms + r0[2]

    return xms, yms, zms
